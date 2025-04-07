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
        Encrypts the given plaintext string using AES CBC mode.
        """
        iv = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_text = pad(plaintext.encode(), AES.block_size)
        ciphertext = cipher.encrypt(padded_text)

        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "iv": base64.b64encode(iv).decode()
        }

    def decrypt(self, b64_ciphertext: str, b64_iv: str):
        """
        Decrypts the base64 encoded ciphertext using the provided IV.
        """
        ciphertext = base64.b64decode(b64_ciphertext)
        iv = base64.b64decode(b64_iv)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted.decode()

    def encrypt_file(self, input_path: str, output_path: str):
        """
        Encrypts a binary file (PDF, DOCX, etc.).
        Saves encrypted binary file with IV prepended to the ciphertext.
        """
        with open(input_path, 'rb') as f:
            file_data = f.read()

        iv = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_data = pad(file_data, AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)

        # Save IV + encrypted content to output file
        with open(output_path, 'wb') as f:
            f.write(iv + encrypted_data)

        logger.info(f"📁 File encrypted and saved to {output_path}")

    def decrypt_file(self, input_path: str, output_path: str):
        """
        Decrypts a previously encrypted binary file.
        Expects IV to be the first 16 bytes of the file.
        """
        with open(input_path, 'rb') as f:
            iv = f.read(16)
            encrypted_data = f.read()

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        with open(output_path, 'wb') as f:
            f.write(decrypted_data)

        logger.info(f"📂 File decrypted and saved to {output_path}")
