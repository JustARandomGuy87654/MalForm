<!--
  Malform Builder – README
-->
<p align="center">
  <img src="https://img.shields.io/badge/version-1.2.2-blue" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8%2B-yellow" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

# 💀 Malform Builder

> _"Hide truths, reveal nothing."_  

> A dual-mode (GUI & CLI) stub builder that embeds scripts, text or PDFs into encrypted, obfuscated payloads.

---

## 🔍 Table of Contents

- [Features](#-features)  
- [Demo](#-demo)  
- [Installation](#-installation)  
- [Usage](#-usage)  
  - [GUI Mode](#gui-mode)  
  - [CLI Mode](#cli-mode)  
- [Examples](#-examples)  
- [Configuration & Options](#-configuration--options)  
- [Under the Hood](#-under-the-hood)  
- [Roadmap](#-roadmap)  
- [Contributing](#-contributing)  
- [License](#-license)  
- [Disclaimer](#-disclaimer)  

---

## ✨ Features

- **Encryption**  
  - `Fernet` (AES-128)  
  - `AES-CBC` (AES-256 + PKCS#7 padding)  
  - PowerShell (Base64 + UTF-16 LE)  
- **Obfuscation**  
  - Reverse Base64 strings (`[::-1]`)  
  - Optional VM-check via `wmic`  
  - Execution delay (custom seconds)  
- **Packaging**  
  - Auto-compile to single EXE with PyInstaller  
  - Verbose or silent builds  
- **Input types**  
  - Python & PowerShell scripts (`.py`, `.ps1`)  
  - Raw text blocks  
  - PDF documents  
- **Dual interface**  
  - Modern dark GUI (CustomTkinter)  
  - Lightweight CLI

---

## 🎬 Demo

<!-- GIF or screenshot link -->
![Malform Builder GUI](docs/demo.gif)

---
