import pickle
import socket

from openzip.networking.crypto.asymmetric import BaseAsymmetricSystem
from openzip.networking.crypto.keysmanager import KeysManager
from openzip.networking.crypto.symmetric import BaseSymmetricSystem
from openzip.networking.messages import Messages
from openzip.utils.constants import DEFAULT_CONNECTION_BUFFER


class Connection:
    def __init__(self, sock: socket.socket, server_side: bool):
        """
        It implements methods to send and recieve encrypted data with another instance of this class.

        It permits a hybrid encryption of the data with RSA 4096 and AES256.

        The buffer size in recieve method (that calls socket.recv()) is 8192 bytes.

        :param sock: the socket to use for the comunication.
        :param server_side: if the socket is returned by socket.accept() set it to True, False otherwise.
        """
        self._sock = sock
        self._keys = KeysManager(asymmetric=BaseAsymmetricSystem(), symmetric=BaseSymmetricSystem())
        self._server_side = server_side
        self._buffer = DEFAULT_CONNECTION_BUFFER

        self.__keys_exchange__()

    def recv(self, decrypt=True) -> bytes:
        """
        Recieve the data from the connected socket (remote) with the socket given in the initializion of this class.

        It can recieve at most 8192 bytes of data for each call.

        :param decrypt: if True use the RSA4096 and AES256 to decrypt the data, if False not decrypt the data.
        :return: the bytes recieved.
        """
        if self._keys is None and decrypt is True:
            raise ValueError("Keys are necessary to decrypt the data.")

        if decrypt:
            # recieve the AES256 serialized cipher encrypted with RSA4096
            encrypted_cipher = self._sock.recv(self._buffer)
            self._sock.send(Messages.packet_received)  # send the confirmation of receipt of the packet

            # recieve the data encrypted with AES256
            encrypted_data = self._sock.recv(self._buffer)
            self._sock.send(Messages.packet_received)

            # decrypt the AES256 serialized cipher with RSA4096
            dumped_cipher = self._keys.rsa.rsa_decrypt(data=encrypted_cipher)
            cipher = pickle.loads(dumped_cipher)  # deserialize the cipher

            # decrypt the data recieved with AES256
            decrypted_data = self._keys.aes.aes_decrypt(encrypted_data=encrypted_data, cipher=cipher)

            return decrypted_data

        else:
            # recieve the data without encrypt it
            data = self._sock.recv(self._buffer)
            self._sock.send(Messages.packet_received)

            return data

    def send(self, data: bytes, encrypt=True):
        """
        Send the data to the connected socket (remote) with the socket given in the initializion of this class.

        :param data: the data to send, not encrypted.
        :param encrypt: if True ecnrypt the data before send it, if False send the data without encrypt it.
        """
        if self._keys is None and encrypt is True:
            raise ValueError("Keys are necessary to encrypt the data.")

        if encrypt:
            # encrypt the data with AES256
            aes_encrypted_data = self._keys.aes.aes_encrypt(data=data)

            # serialize the AES256 cipher
            dumped_aes_cipher = pickle.dumps(obj=self._keys.aes.cipher, protocol=pickle.HIGHEST_PROTOCOL)

            # encrypt the serialized AES256 cipher with RSA4096
            encrypted_cipher = self._keys.rsa.rsa_encrypt(data=dumped_aes_cipher,
                                                          key=self._keys.remote_public_key)

            # first send AES256 encrypted with RSA4096
            self._sock.send(encrypted_cipher)
            assert self._sock.recv(self._buffer) == Messages.packet_received  # confirms the receipt of the packet

            # then send the data encrypted with AES256
            self._sock.send(aes_encrypted_data)
            assert self._sock.recv(self._buffer) == Messages.packet_received

        else:
            # send the data without encrypt it
            self._sock.send(data)
            assert self._sock.recv(self._buffer) == Messages.packet_received

    def close(self):
        self._sock.close()

    def __keys_exchange__(self):
        """
        Exchange the public keys with the remote Connection instance.
        """
        if self._server_side:
            # convert the server's public key to bytes
            server_public_key = self._keys.public_key_to_bytes()
            # send the server's public key not encrypted to the client
            self.send(data=server_public_key, encrypt=False)

            # the client send its encrypted public key (encrypted)
            client_public_key_bytes = self.recv()
            # convert the bytes of the client's public key in its RSAPublicKey object
            client_public_key = self._keys.bytes_to_public_key(data=client_public_key_bytes)

            # set the remote client's public key
            self._keys.remote_public_key = client_public_key

        else:
            # recieve the server's public key bytes not encrypted
            server_public_key_bytes = self.recv(decrypt=False)

            # convert the bytes of the server's public key in its RSAPublicKey object
            server_public_key = self._keys.bytes_to_public_key(server_public_key_bytes)

            # set the remote server's public key
            self._keys.remote_public_key = server_public_key

            # convert the client's public key to bytes
            client_public_key_bytes = self._keys.public_key_to_bytes()
            # send the client's encrypted public key
            self.send(data=client_public_key_bytes)

    @property
    def buffer_size(self) -> int:
        return self._buffer

    @property
    def keys(self) -> KeysManager:
        return self._keys
