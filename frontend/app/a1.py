# aes_app.py
#Test1
import streamlit as st
import json
import base64
from io import BytesIO
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.encryption.aes_handler import AESHandler

# UI Setup
st.set_page_config(page_title="AES Encryption", layout="centered")
st.title("🔐 AES Encryption & Decryption")
st.markdown("Secure your data with dynamic AES key & IV")

aes = AESHandler()

tab1, tab2 = st.tabs(["🔒 Encrypt", "🔓 Decrypt"])

with tab1:
    st.subheader("Enter text to encrypt")
    text_to_encrypt = st.text_area("Plaintext", placeholder="Type your secret message here...")

    if st.button("Encrypt"):
        if text_to_encrypt.strip() != "":
            result = aes.encrypt(text_to_encrypt)
            key_b64 = aes.get_key()

            # Bundle everything into JSON
            json_data = {
                "ciphertext": result['ciphertext'],
                "iv": result['iv'],
                "key": key_b64
            }

            json_bytes = json.dumps(json_data, indent=4).encode("utf-8")

            st.success("✅ Encrypted successfully!")
            st.code(f"Ciphertext (Base64): {result['ciphertext']}", language="text")
            st.code(f"IV (Base64): {result['iv']}", language="text")
            st.code(f"Key (Base64): {key_b64}", language="text")

            st.download_button("⬇️ Download Key File (.json)", data=json_bytes, file_name="aes_key.json", mime="application/json")
        else:
            st.warning("Please enter some text to encrypt.")

with tab2:
    st.subheader("Select decryption method")

    method = st.radio("Key Input Method", ["🔤 Manual Input", "📂 Upload JSON Key File"])

    if method == "🔤 Manual Input":
        b64_ciphertext = st.text_input("Ciphertext (Base64)")
        b64_iv = st.text_input("IV (Base64)")
        b64_key = st.text_input("AES Key (Base64)")
    else:
        uploaded_file = st.file_uploader("Upload Key JSON File", type=["json"])
        b64_ciphertext = b64_iv = b64_key = None

        if uploaded_file:
            try:
                file_contents = json.load(uploaded_file)
                b64_ciphertext = file_contents["ciphertext"]
                b64_iv = file_contents["iv"]
                b64_key = file_contents["key"]
            except Exception as e:
                st.error(f"Invalid JSON format: {e}")

    if st.button("Decrypt"):
        try:
            if b64_ciphertext and b64_iv and b64_key:
                aes_with_key = AESHandler(key=base64.b64decode(b64_key.strip()))
                decrypted_text = aes_with_key.decrypt(b64_ciphertext, b64_iv)
                st.success("✅ Decryption successful!")
                st.code(f"Decrypted Text: {decrypted_text}", language="text")
            else:
                st.warning("Please fill in all required fields or upload a valid key file.")
        except Exception as e:
            st.error(f"❌ Decryption failed: {str(e)}")
