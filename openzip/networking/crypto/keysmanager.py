from typing import Optional

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from openzip.networking.crypto.asymmetric import BaseAsymmetricSystem
from openzip.networking.crypto.symmetric import BaseSymmetricSystem


class KeysManager:
    def __init__(self, asymmetric: BaseAsymmetricSystem, symmetric: BaseSymmetricSystem):
        self.rsa = asymmetric
        self.aes = symmetric
        self._remote_public_key = None

    @property
    def remote_public_key(self) -> Optional[RSAPublicKey]:
        return self._remote_public_key

    @remote_public_key.setter
    def remote_public_key(self, public_key: RSAPublicKey):
        self._remote_public_key = public_key

    def public_key_to_bytes(self) -> bytes:
        data = self.rsa.public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                format=serialization.PublicFormat.SubjectPublicKeyInfo)
        return data

    @staticmethod
    def bytes_to_public_key(data: bytes) -> RSAPublicKey:
        return serialization.load_pem_public_key(data, backend=default_backend())


if __name__ == "__main__":
    keys_manager = KeysManager(asymmetric=BaseAsymmetricSystem(), symmetric=BaseSymmetricSystem())
    pk_bytes = keys_manager.public_key_to_bytes()
    print(pk_bytes)
    pk = keys_manager.bytes_to_public_key(data=pk_bytes)
    print(pk)
