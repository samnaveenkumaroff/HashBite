
# 🔐 HashBite – Franchise-Grade AES Encryption for Text & Files

## 📦 Project Overview

**HashBite** is a powerful, locally running AES-based encryption tool designed to help **franchise-based businesses** (especially in the **Food & Beverage industry**) secure their **secret recipes, documents, and sensitive data**.

The system supports **manual encryption**, **JSON key packaging**, and **secure file handling**, making it ideal for multi-branch companies where the **HQ retains key authority**, and franchises can decrypt only what they’re permitted to — all without using the cloud.

---

## 🌟 Key Features

- 🔐 AES-256 Encryption (CBC Mode)
- 📤 Encrypt/Decrypt text or binary files (PDFs, DOCX, etc.)
- 📁 Downloadable encrypted JSON files with key, IV & metadata
- 📂 Upload JSON key files for secure decryption
- 🖥️ Streamlit-powered local GUI — no cloud, no API required
- 🔄 Dual-mode key input (manual or key file upload)
- 💼 Tailored for franchise communication and controlled recipe distribution

---

## 📂 Project Structure

```
HashBite/
├── backend/
│   ├── encryption/
│   │   ├── __init__.py
│   │   └── aes_handler1.py         # Core AES encryption/decryption logic
│
├── frontend/
│   └── app/
│       └── a2.py                   # Streamlit UI for text and file encryption
│
├── data/
│   ├── recipes/
│   └── encrypted/
│
├── tests/
│   └── test_aes.py
│
├── requirements.txt               # Dependencies
├── README.md                      # This documentation
└── .gitignore
```

---

## 🔑 Key Components

### 1. `aes_handler1.py`

- Handles AES encryption/decryption in CBC mode
- Supports:
  - `encrypt()`, `decrypt()` for text
  - `encrypt_file()`, `decrypt_file()` for binary files
- Uses IV and PKCS7 padding
- Key is returned/stored in Base64

### 2. `a2.py` (Streamlit UI)

- Clean tabbed interface
- Tabs:
  - `Encrypt/Decrypt Text`
  - `Encrypt Files`
  - `Decrypt Files`
- Allows file encryption and decryption using `.json` packages

---

## 🛠 Technical Requirements

### ✅ System

- OS: Ubuntu / Windows / macOS
- RAM: 4GB+ recommended
- Python 3.10+

### ✅ Python Libraries

- `pycryptodome`
- `streamlit`

Install via:

```bash
pip install -r requirements.txt
```

---

## 🔧 Setup & Installation

### 1. Clone the Project

```bash
git clone https://github.com/samnaveenkumaroff/HashBite.git
cd HashBite
```

### 2. Create & Activate Conda Environment

```bash
conda create -n hashbite_env python=3.10
conda activate hashbite_env
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run frontend/app/a2.py
```

---

## 🔒 How It Works

### 🔤 Text Encryption

1. Type your secret text
2. Click **Encrypt**
3. Download the `.json` key file

### 📁 File Encryption

1. Upload a file (PDF, DOCX, etc.)
2. Click **Encrypt File**
3. Download `.json` file with:
   - Ciphertext
   - IV
   - Key
   - Original Filename
   - MIME type

### 📂 File Decryption

1. Upload the `.json` key file
2. Click **Decrypt File**
3. Download original decrypted file

---

## 🧠 Franchise Use Case

- 🍔 HQ encrypts the **recipe** and sends `.json` file to **franchise**
- 🧑‍🍳 Franchise decrypts using the file inside **HashBite UI**
- 📦 No source file ever exposed
- 🔐 Key & IV stay hidden unless explicitly shared

---

## 🔐 Security Considerations

- AES-256 with random IV for each encryption
- No key stored — it's passed securely via `.json`
- Supports **zero-knowledge** sharing across branches
- Local-first: everything stays on your device

---

## 🧪 Test the Encryption

Run unit tests:

```bash
python tests/test_aes.py
```

---

## ✨ Future Enhancements

- ✅ Role-based access control using ABE
- ✅ Visual dashboard for file/key management
- 🌐 Secure LAN-based franchise key server (optional)
- 📱 Mobile interface with QR code key import

---

## 🧾 License

Apache 2.0 License

---

## 👨‍💻 Authors

**Sam Naveenkumar V**  
Email: [samnaveenkumaroff@gmail.com](mailto:samnaveenkumaroff@gmail.com)  
GitHub: [@samnaveenkumaroff](https://github.com/samnaveenkumaroff)


---

## 🙏 Acknowledgements

- Karunya Institute of Technology and Sciences
- Vaseegrah Veda Innovation Cell
- Open Source Python Community
- Streamlit & PyCryptodome Contributors

---

Let me know if you'd like this in `README.md` format ready to paste or push!
