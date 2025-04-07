from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def pad(data):
    return data + b"\0" * (AES.block_size - len(data) % AES.block_size)

def encrypt(plain_text, key):
    plain_text = pad(plain_text.encode())
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(plain_text)
    return base64.b64encode(encrypted).decode()

def decrypt(cipher_text, key):
    cipher_text = base64.b64decode(cipher_text)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(cipher_text)
    return decrypted.rstrip(b"\0").decode()

if __name__ == "__main__":
    key = b"This is a key123"  # 16 bytes
    message = "HashBite Rocks!"

    encrypted_msg = encrypt(message, key)
    print("Encrypted:", encrypted_msg)

    decrypted_msg = decrypt(encrypted_msg, key)
    print("Decrypted:", decrypted_msg)
