import os.path
import pickle
import queue
import socket
import time

from openzip.bruteforce.brutezip import OpenZipWithBruteforce
from openzip.networking.crypto.connection import Connection
from openzip.networking.messages import Messages
from openzip.networking.netinfo import NetworkInfo
from openzip.utils._threading import deamon_thread
from openzip.utils.constants import MAX_CPU_PROCESSES, DEFAULT_SERVER_PORT
from openzip.utils.identifiers import new_client_id
from openzip.utils.paths import TEMP_DIR


class Client:
    def __init__(self, server_ip: str, nprocesses: int, client_id: str = None):
        """
        A Client can be connected with a ZipServer to recieve the encrypted zip file
        and the password's generators.
        It will automatically test all the passowords generated and send back the correct password to the
        ZipServer if it is found.

        :param server_ip: the ip to connect the client's socket.
        :param nprocesses: number of processes to start, should be at most the same value returned by os.cpu_count().
        """
        assert 1 <= nprocesses <= MAX_CPU_PROCESSES, f"You can run at most {MAX_CPU_PROCESSES} processes"

        self._server_address = (server_ip, DEFAULT_SERVER_PORT)
        self._nprocesses = nprocesses

        self._server_id = None
        self._client_id = client_id or new_client_id()

        self._filepath = str()
        self._generator = None

        self._file_download_percentage = float(0)
        self._queue_messages = queue.SimpleQueue()
        self._password = None
        self._is_running = True

        self.ozwb = None

        self._client_sock = socket.socket()
        self._client_sock.connect(self._server_address)

        self._client_sock.send(Messages.login)

        try:
            self._connection = Connection(sock=self._client_sock, server_side=False)

        except ValueError:  # the keys cannot be exchanged because the server closed the socket (clients limit reached)
            raise ConnectionError("The server is full.")

    @deamon_thread
    def start(self):
        """
        Start the comunication with the ZipServer.
        Receive the encrypted zip file and the password's generator, start the cracking process
        and handle messages at runtime.
        """
        self._server_id = self._connection.recv().decode()
        self._connection.send(self._client_id.encode())

        self.__recv_file__()
        self.__recv_pwd_gen__()
        self.__start_bruteforce__()
        self.__messages_handler__()

    def __messages_handler__(self):
        """
        Handle the messages from the client and the server every 10 seconds
        if there is nothing to do.
        """
        while self._is_running:
            if self._queue_messages.empty():
                self._queue_messages.put(Messages.keep_connection_alive)

            client_msg = self._queue_messages.get()  # get the first message inserted in queue
            self._connection.send(client_msg)

            server_msg = self._connection.recv()

            if client_msg == server_msg == Messages.password_found:
                # this client have found the password
                self.__send_pwd_found__()

            elif server_msg == Messages.password_found:
                # another client found the password, stop this client
                self.__stop__()

            elif client_msg == server_msg == Messages.next_password_generator:
                self.__recv_pwd_gen__()
                self.__start_bruteforce__()

            elif client_msg == server_msg == Messages.keep_connection_alive:
                # nothing to do, just wait 10 seconds to prevent to send too many data
                time.sleep(10)

            else:
                raise ValueError(f"Unknow message from the server: {server_msg}")

    def __recv_file__(self):
        """
        Receve the file from the server and save it in a temporany directory
        with the format: ID-NAME.
        """
        filesize = int(self._connection.recv().decode())
        filename = self._connection.recv().decode()
        filename = f"{self._client_id}-{filename}"
        self._filepath = os.path.join(TEMP_DIR, filename)

        bytes_received = 0
        with open(self._filepath, "wb") as f:
            while True:
                data_packet = self._connection.recv()
                if data_packet == Messages.transmission_complete:
                    break

                else:
                    bytes_received += len(data_packet)
                    self._file_download_percentage = f"{(bytes_received / filesize) * 100:.2f}".zfill(5)
                    f.write(data_packet)

    def __recv_pwd_gen__(self):
        """
        Receive the password's generator from the server, if the server responds with a
        "no_generator_available" massage stop the client and close the connection.
        """
        if (dumped_generator := self._connection.recv()) != Messages.no_generator_available:
            self._generator = pickle.loads(dumped_generator)

        else:
            self._generator = None
            self._is_running = False

            self._connection.close()

    def __send_pwd_found__(self):
        self._connection.send(self._password.encode())
        self.__stop__()

    def __set_pwd__(self, pwd: str):
        self._password = pwd
        self._queue_messages.put(Messages.password_found)

    @deamon_thread
    def __start_bruteforce__(self):
        if self._generator:
            self.ozwb = OpenZipWithBruteforce(filepath=self._filepath,
                                              pwd_generator=self._generator,
                                              on_found_callback=self.__set_pwd__,
                                              nprocesses=self._nprocesses)

            self._queue_messages.put(Messages.next_password_generator)

    def __stop__(self):
        """
        Remove the temporany file and close the connection.
        """
        os.remove(path=self._filepath)
        self._connection.close()
        self._is_running = False

    @property
    def file_download_percentage(self) -> float:
        return self._file_download_percentage

    @property
    def is_running(self) -> bool:
        return self._is_running
