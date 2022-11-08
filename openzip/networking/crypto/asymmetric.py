from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey


class BaseAsymmetricSystem:
    """
    Implement asymmetric keys with RSA-4096.

    It contains methods to encrypy and decrypt the data.
    """
    def __init__(self):
        self._private_key = rsa.generate_private_key(key_size=4096, public_exponent=65537, backend=default_backend())
        self._public_key = self._private_key.public_key()
        self._padding = OAEP(mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)

    @property
    def public_key(self) -> RSAPublicKey:
        return self._public_key

    def rsa_decrypt(self, data: bytes) -> bytes:
        return self._private_key.decrypt(ciphertext=data, padding=self._padding)

    def rsa_encrypt(self, data: bytes, key: RSAPublicKey) -> bytes:
        return key.encrypt(plaintext=data, padding=self._padding)


if __name__ == "__main__":
    bas = BaseAsymmetricSystem()
    print(bas.public_key)
