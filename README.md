# MalForm - Educational Malware Encrypter

![Warning](https://img.shields.io/badge/Warning-Educational%20Use%20Only-red)

---

## ⚠️ Disclaimer

**Malform** is a script made by a me for educacional uses, and i'm not responsable of what you are going to do with it.

---

## Features

- 🔐 Encrypted payloads using **Fernet** or **AES-CBC**
- 🧪 Built-in **Anti‑VM** checks (blocks execution on virtual machines)
- ⏱ Customizable **execution delay** before payload runs
- 📦 Automatic `.exe` compilation using **PyInstaller**
- 🖼️ Modern GUI built with **CustomTkinter**

---

## Setup & Usage

1. git clone https://github.com/JustARandomGuy87654/MalForm
2. pip3 install cryptography pycryptodome customtkinter pyinstaller
3. **python3 malform.py** | If you want to use the CLI mode then use: **python malform.py your_script_name -m encryption_you_want_to_use --anti-vm --delay secounds --verbose**
4. Then it will build you encrypted malware, **the automatic exe build is bugged right now.**

---

## Futures ideas
1. More encryption methods
3. More robust powershell encryption
5. Correct the exe builder bug
If you have any more idea, DM me on discord: justarandomguy62

---
