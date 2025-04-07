# backend/encryption/aes_handler.py

import os
import base64
import logging
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class AESHandler:
    def __init__(self, key: bytes = None):
        """
        Initializes AES Handler with a 32-byte key.
        If no key is provided, a new one is generated.
        """
        self.key = key or os.urandom(32)
        logger.info("🔑 AES key generated or provided.")

    def get_key(self):
        """
        Returns the AES key in base64 format.
        """
        b64_key = base64.b64encode(self.key).decode()
        logger.debug(f"🔐 AES Key (Base64): {b64_key}")
        return b64_key

    def encrypt(self, plaintext: str):
        """
        Encrypts the given plaintext using AES CBC mode.
        Returns a dictionary with base64 ciphertext and IV.
        """
        iv = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_text = pad(plaintext.encode(), AES.block_size)
        ciphertext = cipher.encrypt(padded_text)

        b64_cipher = base64.b64encode(ciphertext).decode()
        b64_iv = base64.b64encode(iv).decode()

        logger.info("🔒 Encryption completed.")
        logger.debug(f"📦 Ciphertext (Base64): {b64_cipher}")
        logger.debug(f"🌀 IV (Base64): {b64_iv}")

        return {
            "ciphertext": b64_cipher,
            "iv": b64_iv
        }

    def decrypt(self, b64_ciphertext: str, b64_iv: str):
        """
        Decrypts the ciphertext using the provided IV.
        Returns the original plaintext.
        """
        ciphertext = base64.b64decode(b64_ciphertext)
        iv = base64.b64decode(b64_iv)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)

        logger.info("🔓 Decryption completed.")
        logger.debug(f"📄 Decrypted text: {decrypted.decode()}")
        return decrypted.decode()
