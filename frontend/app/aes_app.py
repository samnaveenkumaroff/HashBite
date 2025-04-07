# aes_app.py

import sys
import os
import base64
import streamlit as st

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.encryption.aes_handler import AESHandler

# Streamlit UI setup
st.set_page_config(page_title="AES Encryption", layout="centered")
st.title("🔐 HashBite AES Encryption & Decryption")
st.markdown("Secure your Recipes with dynamic AES key & IV")

# Initialize AESHandler with a random key
aes = AESHandler()

tab1, tab2 = st.tabs(["🔒 Encrypt", "🔓 Decrypt"])

with tab1:
    st.subheader("Enter text to encrypt")
    text_to_encrypt = st.text_area("Plaintext", placeholder="Type your secret message here...")

    if st.button("Encrypt"):
        if text_to_encrypt.strip() != "":
            result = aes.encrypt(text_to_encrypt)
            st.success("✅ Encrypted successfully!")
            st.code(f"Ciphertext (Base64): {result['ciphertext']}", language="text")
            st.code(f"IV (Base64): {result['iv']}", language="text")
            st.code(f"Key (Base64): {aes.get_key()}", language="text")
        else:
            st.warning("Please enter some text to encrypt.")

with tab2:
    st.subheader("Enter encrypted values to decrypt")
    b64_ciphertext = st.text_input("Ciphertext (Base64)")
    b64_iv = st.text_input("IV (Base64)")
    b64_key = st.text_input("AES Key (Base64)")

    if st.button("Decrypt"):
        try:
            if b64_ciphertext and b64_iv and b64_key:
                # Reuse AESHandler with provided key
                aes_with_key = AESHandler(key=base64.b64decode(b64_key))
                decrypted_text = aes_with_key.decrypt(b64_ciphertext, b64_iv)
                st.success("✅ Decryption successful!")
                st.code(f"Decrypted Text: {decrypted_text}", language="text")
            else:
                st.warning("Please fill in all fields to decrypt.")
        except Exception as e:
            st.error(f"❌ Decryption failed: {str(e)}")
