import os
import pickle
from typing import Optional

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class BaseSymmetricSystem:
    """
    Implement symmetric key with AES-256.

    It contains methods to encrypy and decrypt the data.
    """
    def __init__(self):
        self._cipher = None

    def aes_encrypt(self, data: bytes) -> bytes:
        self.__new_cipher__()

        padder = padding.PKCS7(block_size=256).padder()

        encryptor = self._cipher.encryptor()
        padded_data = padder.update(data) + padder.finalize()
        padded_encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        return padded_encrypted_data

    def aes_decrypt(self, encrypted_data: bytes, cipher: Cipher = None) -> bytes:
        if cipher is None:
            cipher = self._cipher

        unpadder = padding.PKCS7(block_size=256).unpadder()

        decryptor = cipher.decryptor()
        padded_decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadded_decrypted_data = unpadder.update(padded_decrypted_data) + unpadder.finalize()

        return unpadded_decrypted_data

    @property
    def cipher(self) -> Optional[Cipher]:
        return self._cipher

    def __new_cipher__(self):
        key = os.urandom(32)
        iv = os.urandom(16)
        cipher = Cipher(algorithm=algorithms.AES256(key), mode=modes.CBC(iv))
        self._cipher = cipher


if __name__ == "__main__":
    payload = os.urandom(4096 - 32)
    bss = BaseSymmetricSystem()
    encrypted_payload = bss.aes_encrypt(data=payload)
    decrypted_payload = bss.aes_decrypt(encrypted_data=encrypted_payload)
    dumped_cipher = pickle.dumps(obj=bss.cipher, protocol=pickle.HIGHEST_PROTOCOL)

    print("Payload:", payload)
    print("Encrypted payload:", encrypted_payload)
    print("Decrypted payload:", decrypted_payload)
    print("Payload size (bytes):", len(payload))
    print("Encrypted payload size (bytes):", len(encrypted_payload))
    print("Decrypted payload size (bytes):", len(decrypted_payload))
    print("Dumped cipher size (bytes):", len(dumped_cipher))
