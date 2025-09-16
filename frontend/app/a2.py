#Test 2
import streamlit as st
import base64
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.encryption.aes_handler1 import AESHandler  # Updated import

st.set_page_config(page_title="AES Encryption", layout="centered")
st.title("🔐 AES Encryption & Decryption")
st.markdown("Secure your text and files (📄PDF, 📃DOC, and others) with AES encryption")

aes = AESHandler()

tabs = st.tabs(["🔤 Text Encrypt/Decrypt", "📁 File Encrypt", "📂 File Decrypt"])

# TEXT ENCRYPT/DECRYPT TAB
with tabs[0]:
    sub_tab1, sub_tab2 = st.tabs(["🔒 Encrypt Text", "🔓 Decrypt Text"])

    with sub_tab1:
        st.subheader("Enter text to encrypt")
        text_to_encrypt = st.text_area("Plaintext")

        if st.button("Encrypt Text"):
            if text_to_encrypt.strip():
                result = aes.encrypt(text_to_encrypt)
                key_b64 = aes.get_key()
                json_data = {
                    "ciphertext": result['ciphertext'],
                    "iv": result['iv'],
                    "key": key_b64
                }
                json_bytes = json.dumps(json_data, indent=4).encode("utf-8")

                st.success("✅ Text Encrypted")
                st.download_button("⬇️ Download Key File (.json)", data=json_bytes, file_name="text_encryption_key.json", mime="application/json")
            else:
                st.warning("Please enter text.")

    with sub_tab2:
        method = st.radio("Key Input Method", ["🔤 Manual Input", "📂 Upload JSON Key File"])
        b64_ciphertext = b64_iv = b64_key = None

        if method == "🔤 Manual Input":
            b64_ciphertext = st.text_input("Ciphertext (Base64)")
            b64_iv = st.text_input("IV (Base64)")
            b64_key = st.text_input("AES Key (Base64)")
        else:
            uploaded_file = st.file_uploader("Upload Key File (.json)", type=["json"])
            if uploaded_file:
                try:
                    data = json.load(uploaded_file)
                    b64_ciphertext, b64_iv, b64_key = data["ciphertext"], data["iv"], data["key"]
                except:
                    st.error("Invalid JSON file")

        if st.button("Decrypt Text"):
            try:
                if b64_ciphertext and b64_iv and b64_key:
                    aes_with_key = AESHandler(key=base64.b64decode(b64_key))
                    plaintext = aes_with_key.decrypt(b64_ciphertext, b64_iv)
                    st.success("✅ Text Decrypted")
                    st.code(plaintext)
                else:
                    st.warning("Missing inputs or file.")
            except Exception as e:
                st.error(f"❌ Decryption failed: {e}")

# FILE ENCRYPTION TAB
with tabs[1]:
    st.subheader("📁 Upload a file to encrypt")
    uploaded_file = st.file_uploader("Choose a file (PDF, DOCX, TXT, etc.)", type=None, key="encrypt_file")

    if uploaded_file and st.button("Encrypt File"):
        try:
            file_bytes = uploaded_file.read()
            result = aes.encrypt(file_bytes.decode("latin-1"))  # Using latin-1 for binary-safe text encoding

            json_data = {
                "ciphertext": result['ciphertext'],
                "iv": result['iv'],
                "key": aes.get_key(),
                "filename": uploaded_file.name,
                "mimetype": uploaded_file.type
            }

            json_bytes = json.dumps(json_data, indent=4).encode("utf-8")
            st.success("✅ File encrypted successfully!")
            st.download_button("⬇️ Download Encrypted JSON", data=json_bytes, file_name=f"{uploaded_file.name}.json", mime="application/json")

        except Exception as e:
            st.error(f"Encryption failed: {e}")

# FILE DECRYPTION TAB
with tabs[2]:
    st.subheader("📂 Upload encrypted JSON file to decrypt original file")
    file_key_upload = st.file_uploader("Upload Encrypted JSON File", type=["json"], key="decrypt_file")

    if file_key_upload and st.button("Decrypt File"):
        try:
            data = json.load(file_key_upload)
            key = base64.b64decode(data["key"])
            iv = data["iv"]
            ciphertext = data["ciphertext"]
            filename = data.get("filename", "decrypted_file")
            mimetype = data.get("mimetype", "application/octet-stream")

            aes_with_key = AESHandler(key=key)
            decrypted_text = aes_with_key.decrypt(ciphertext, iv)

            decrypted_bytes = decrypted_text.encode("latin-1")  # Convert back to binary
            st.success(f"✅ File decrypted: {filename}")
            st.download_button(f"⬇️ Download Decrypted File", data=decrypted_bytes, file_name=f"decrypted_{filename}", mime=mimetype)

        except Exception as e:
            st.error(f"❌ Decryption failed: {e}")
