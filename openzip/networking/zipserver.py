import os.path
import pickle
import socket
import time
from typing import Tuple, Union, List, NamedTuple

import pyzipper

from openzip.networking.crypto.connection import Connection
from openzip.networking.messages import Messages
from openzip.networking.netinfo import NetworkInfo
from openzip.utils._threading import deamon_thread
from openzip.utils.constants import MAX_DEFAULT_CLIENTS, DEFAULT_CONNECTION_BUFFER, DEFAULT_SERVER_PORT
from openzip.utils.identifiers import new_server_id
from openzip.utils.passwords import PasswordsManager


class PasswordInfo(NamedTuple):
    """
    Store the password's information of a zip file.

    - pwd: the password
    - client_id: the client's id who found the password
    - localtime: the time on when the password is received
    """
    pwd: str
    client_id: str
    localtime: time.struct_time


class ZipServer:
    def __init__(self,
                 filepath: str,
                 charset: Union[List[str], str],
                 pwd_min_len: int,
                 pwd_max_len: int,
                 max_clients: int = MAX_DEFAULT_CLIENTS):
        """
        ZipServer hosts the encrypted zip file and the password generators, it also distributes the work
        over all the clients connected.

        :param filepath: the path of th file zip
        :param charset: the charset to use against the encrypted zip
        :param pwd_min_len: minimum length of the password
        :param pwd_max_len: maximum length of the password
        :param max_clients: max number of clients accepted, the connection will close automatically for new clients
        """

        assert os.path.exists(filepath), "The zip file not exists."
        assert pyzipper.is_zipfile(filepath), "The file is not a zip file."

        self._filepath = filepath
        self._server_id = new_server_id()
        self.max_clients = max_clients
        self._passwords_manager = PasswordsManager(charset=charset,
                                                   pwd_min_len=pwd_min_len,
                                                   pwd_max_len=pwd_max_len,
                                                   split_in=max_clients)

        self._server_sock = socket.socket()
        self._server_ip = NetworkInfo().local_ipv4
        self._server_port = DEFAULT_SERVER_PORT

        self.password_found = False
        self.password_info = None
        self._is_running = True

        self.clients: List[ClinetHandler] = list()

    @deamon_thread
    def start(self):
        """
        Create a socket in server mode ad accept new connections from the clients.

        If the number of connected clients is greater than max_clients, a new
        connection attempt will be closed automatically.
        """

        self.__state_monitoring__()

        self._server_sock = socket.socket()
        self._server_sock.bind((self._server_ip, self._server_port))
        self._server_sock.listen()

        while self._is_running:
            try:
                client_sock, client_addr = self._server_sock.accept()

            except OSError:
                # OSError occur when the socket is closed by self.__state_monitoring__()
                break

            # the client send the reason of the connection: Messages.login or Messages.scan
            connection_reason = client_sock.recv(DEFAULT_CONNECTION_BUFFER)

            if connection_reason == Messages.login:
                if len(self.clients) >= self.max_clients:
                    client_sock.close()

                else:
                    new_client_handler = ClinetHandler(server=self, client_sock=client_sock, client_addr=client_addr)
                    self.clients.append(new_client_handler)

            elif connection_reason == Messages.scan:
                client_sock.send(self.server_id.encode())

            else:
                raise ValueError(f"Bad connection_reason {connection_reason}")

    def stop(self):
        self._is_running = False
        self._server_sock.close()

    @deamon_thread
    def __state_monitoring__(self):
        """
        Monitoring if the password is found, if the password is found close the connection with all the clients.
        """
        while self._is_running:
            if self.password_found:
                self._is_running = False
                self._server_sock.close()

            else:
                time.sleep(1)

    @property
    def server_ip(self) -> str:
        return self._server_ip

    @property
    def server_port(self) -> int:
        return self._server_port

    @property
    def server_id(self) -> str:
        return self._server_id

    @property
    def filepath(self) -> str:
        return self._filepath

    @property
    def passwords_manager(self) -> PasswordsManager:
        return self._passwords_manager

    @property
    def is_running(self):
        return self._is_running

    @is_running.setter
    def is_running(self, value: bool):
        self._is_running = value


class ClinetHandler:
    def __init__(self, server: ZipServer, client_sock: socket.socket, client_addr: Tuple[str, int]):
        # noinspection GrazieInspection
        """
        ClientHandler manages a single client connection, it provides a secure connection encrypting the data with
        RSA4096 and AES256, it provides to send the encrypted zip file to the client and manages all the requests of
        the client.

        For example a client could request a new password generator because it has terminated the previous
        one, so the ClientHandler will check if there are generators available and if there is, it will
        send it to the client.

        :param server: the server that initialized the ClientHandler
        :param client_sock: the socket returned by socket.accept() from the server
        :param client_addr: the tuple (IP, PORT) of the client
        """
        self._server = server
        self._client_sock = client_sock
        self._client_addr = client_addr

        self._is_running = True
        self._client_id = None

        self._connection = Connection(sock=client_sock, server_side=True)

        self.__client_initializing__()

    @deamon_thread
    def __client_initializing__(self):
        """
        Exchange the IDs, send the file, send the passwords generator and handle the client's requests.
        """
        self.__exchange_ids__()
        self.__send_file__()
        self.__send_generator__()

        try:
            self.__messages_handler__()

        except ConnectionAbortedError:
            pass

    def __messages_handler__(self):
        """
        Handle the client's requests until this instance is running.

        The client send a request (message) and the connection will respond accordingly to the type of
        the requests.
        """
        while self._is_running:
            client_msg = self._connection.recv()

            if self._server.password_found:  # first check if the password is found
                self._connection.send(Messages.password_found)
                self._is_running = False

            elif client_msg == Messages.keep_connection_alive:
                self._connection.send(data=Messages.keep_connection_alive)

            elif client_msg == Messages.next_password_generator:
                self._connection.send(data=Messages.next_password_generator)
                self.__send_generator__()

            elif client_msg == Messages.password_found:
                self._connection.send(Messages.password_found)
                self.__set_zipserver_pwd__()

            else:
                raise ValueError(f"Unknow message from the client: {client_msg}")

        self._connection.close()

    def __exchange_ids__(self):
        self._connection.send(data=self._server.server_id.encode())
        self._client_id = self._connection.recv().decode()

    def __send_file__(self):
        """
        Send the file to the remote client.

        - send the size of the file in bytes
        - send the name of the file
        - send the data of the file split in chunks
        - send the end message (transmission complete)
        """
        filesize = str(os.path.getsize(self._server.filepath)).encode()
        filename = self._server.filepath.split(r"/")[-1].encode()

        self._connection.send(data=filesize)
        self._connection.send(data=filename)

        with open(self._server.filepath, "rb") as f:
            while data := f.read(self._connection.buffer_size - 32):  # 32 is the size of the key in AES256
                self._connection.send(data=data)

        self._connection.send(data=Messages.transmission_complete)

    def __set_zipserver_pwd__(self):
        self._server.password_info = PasswordInfo(pwd=self._connection.recv().decode(),
                                                  client_id=self._client_id,
                                                  localtime=time.localtime())

        self._server.password_found = True
        self._is_running = False

    def __send_generator__(self):
        """
        Send the next password's generator, if available, to the client.

        When the remote client finish to iterate over its password's generator,
        it will ask for a new one to the server.
        This function provide to send the next generator to the client.
        """
        if generator := self._server.passwords_manager.get_next_generator():
            dumped_generator = pickle.dumps(obj=generator, protocol=pickle.HIGHEST_PROTOCOL)
            self._connection.send(data=dumped_generator)

        else:
            self._connection.send(data=Messages.no_generator_available)
            self._is_running = False

    @property
    def is_running(self) -> bool:
        return self._is_running

    @property
    def client_id(self) -> str:
        return self._client_id

    @property
    def client_addr(self) -> tuple:
        return self._client_addr

    def __eq__(self, other):
        return True if self._client_id == other.client_id else False
