#!/usr/bin/env python3
"""
Telnet Password Tester - GUI Version
Professional tool for testing passwords against network cameras via Telnet
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import telnetlib
import threading
import time
import os
import sys


class TelnetCrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Telnet Password Tester v1.0")
        self.root.geometry("680x620")
        self.root.minsize(600, 520)
        self.root.configure(bg="#f0f0f0")

        self.running = False
        self.stop_flag = False
        self.passwords = []
        self.found_password = None

        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Main.TFrame", background="#f0f0f0")
        style.configure("Group.TLabelframe", background="#f0f0f0", foreground="#333333",
                         font=("Segoe UI", 9))
        style.configure("Group.TLabelframe.Label", background="#f0f0f0", foreground="#333333",
                         font=("Segoe UI", 9, "bold"))
        style.configure("TLabel", background="#f0f0f0", foreground="#222222",
                         font=("Segoe UI", 9))
        style.configure("Status.TLabel", background="#f0f0f0", foreground="#555555",
                         font=("Segoe UI", 9))
        style.configure("Result.TLabel", background="#dff0d8", foreground="#3c763d",
                         font=("Segoe UI", 10, "bold"))
        style.configure("ResultFail.TLabel", background="#f2dede", foreground="#a94442",
                         font=("Segoe UI", 10, "bold"))
        style.configure("Start.TButton", font=("Segoe UI", 9, "bold"))
        style.configure("Stop.TButton", font=("Segoe UI", 9))
        style.configure("Browse.TButton", font=("Segoe UI", 9))
        style.configure("TProgressbar", troughcolor="#e0e0e0", background="#0078d4",
                         thickness=18)

    def build_ui(self):
        main = ttk.Frame(self.root, style="Main.TFrame")
        main.pack(fill="both", expand=True, padx=10, pady=8)

        # ── Connection ──
        conn = ttk.LabelFrame(main, text=" Connection ", style="Group.TLabelframe")
        conn.pack(fill="x", pady=(0, 6))

        row1 = ttk.Frame(conn, style="Main.TFrame")
        row1.pack(fill="x", padx=10, pady=(8, 4))

        ttk.Label(row1, text="Host:").pack(side="left")
        self.host_var = tk.StringVar(value="192.168.1.15")
        tk.Entry(row1, textvariable=self.host_var, width=18, font=("Segoe UI", 9),
                 relief="solid", bd=1).pack(side="left", padx=(4, 14))

        ttk.Label(row1, text="Port:").pack(side="left")
        self.port_var = tk.StringVar(value="23")
        tk.Entry(row1, textvariable=self.port_var, width=6, font=("Segoe UI", 9),
                 relief="solid", bd=1).pack(side="left", padx=(4, 14))

        ttk.Label(row1, text="Username:").pack(side="left")
        self.user_var = tk.StringVar(value="root")
        tk.Entry(row1, textvariable=self.user_var, width=12, font=("Segoe UI", 9),
                 relief="solid", bd=1).pack(side="left", padx=(4, 14))

        ttk.Label(row1, text="Timeout:").pack(side="left")
        self.timeout_var = tk.StringVar(value="5")
        tk.Entry(row1, textvariable=self.timeout_var, width=4, font=("Segoe UI", 9),
                 relief="solid", bd=1).pack(side="left", padx=(4, 4))
        ttk.Label(row1, text="sec").pack(side="left")

        # ── Password List ──
        pwd = ttk.LabelFrame(main, text=" Password List ", style="Group.TLabelframe")
        pwd.pack(fill="x", pady=(0, 6))

        row2 = ttk.Frame(pwd, style="Main.TFrame")
        row2.pack(fill="x", padx=10, pady=(8, 4))

        ttk.Label(row2, text="File:").pack(side="left")
        self.file_var = tk.StringVar(value="passwords.txt")
        tk.Entry(row2, textvariable=self.file_var, width=44, font=("Segoe UI", 9),
                 relief="solid", bd=1).pack(side="left", padx=(4, 6))
        ttk.Button(row2, text="Browse...", command=self.browse_file,
                   style="Browse.TButton").pack(side="left")

        row3 = ttk.Frame(pwd, style="Main.TFrame")
        row3.pack(fill="x", padx=10, pady=(2, 8))

        ttk.Label(row3, text="Delay between attempts:").pack(side="left")
        self.delay_var = tk.StringVar(value="0.3")
        tk.Entry(row3, textvariable=self.delay_var, width=5, font=("Segoe UI", 9),
                 relief="solid", bd=1).pack(side="left", padx=(4, 4))
        ttk.Label(row3, text="seconds").pack(side="left")

        # ── Buttons ──
        bf = ttk.Frame(main, style="Main.TFrame")
        bf.pack(fill="x", pady=(0, 6))

        self.start_btn = ttk.Button(bf, text="Start", command=self.start_attack,
                                    style="Start.TButton", width=14)
        self.start_btn.pack(side="left")

        self.stop_btn = ttk.Button(bf, text="Stop", command=self.stop_attack,
                                   style="Stop.TButton", width=14, state="disabled")
        self.stop_btn.pack(side="left", padx=(6, 0))

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(bf, textvariable=self.status_var, style="Status.TLabel").pack(side="right")

        # ── Progress ──
        pf = ttk.Frame(main, style="Main.TFrame")
        pf.pack(fill="x", pady=(0, 2))

        self.progress_var = tk.DoubleVar(value=0)
        self.progress = ttk.Progressbar(pf, variable=self.progress_var, maximum=100)
        self.progress.pack(fill="x", side="left", expand=True)

        self.progress_text = tk.StringVar(value="")
        ttk.Label(pf, textvariable=self.progress_text, width=14, anchor="e").pack(
            side="right", padx=(6, 0))

        # ── Result (hidden until needed) ──
        self.result_frame = ttk.Frame(main, style="Main.TFrame")
        self.result_var = tk.StringVar(value="")
        self.result_label = ttk.Label(self.result_frame, textvariable=self.result_var,
                                      style="Result.TLabel", anchor="center")
        self.result_label.pack(fill="x", ipady=6)

        # ── Log ──
        self.log_group = ttk.LabelFrame(main, text=" Log ", style="Group.TLabelframe")
        self.log_group.pack(fill="both", expand=True, pady=(4, 0))

        self.log = scrolledtext.ScrolledText(
            self.log_group, bg="white", fg="#222222", font=("Consolas", 9),
            relief="solid", bd=1, wrap="word", state="disabled", height=14
        )
        self.log.pack(fill="both", expand=True, padx=6, pady=6)

        self.log.tag_configure("ok", foreground="#2e7d32")
        self.log.tag_configure("fail", foreground="#999999")
        self.log.tag_configure("info", foreground="#0078d4")
        self.log.tag_configure("error", foreground="#c62828")
        self.log.tag_configure("found", foreground="#2e7d32", font=("Consolas", 10, "bold"))

    def browse_file(self):
        path = filedialog.askopenfilename(
            title="Select password file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if path:
            self.file_var.set(path)

    def log_msg(self, msg, tag=None):
        self.log.configure(state="normal")
        if tag:
            self.log.insert("end", msg + "\n", tag)
        else:
            self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def load_passwords(self, filename):
        if not os.path.exists(filename):
            return None
        passwords = []
        seen = set()
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line not in seen:
                    passwords.append(line)
                    seen.add(line)
        return passwords

    def test_password(self, host, port, username, password, timeout):
        try:
            tn = telnetlib.Telnet(host, port, timeout=timeout)
            tn.read_until(b"login: ", timeout=timeout)
            tn.write(username.encode("ascii") + b"\n")
            tn.read_until(b"assword:", timeout=timeout)
            tn.write(password.encode("ascii") + b"\n")
            time.sleep(1)
            response = tn.read_very_eager().decode("ascii", errors="ignore")
            if "#" in response or "$ " in response or ">" in response:
                if "incorrect" not in response.lower() and "failed" not in response.lower():
                    tn.close()
                    return True
            tn.close()
            return False
        except Exception:
            return False

    def start_attack(self):
        if self.running:
            return

        pwd_file = self.file_var.get().strip()
        passwords = self.load_passwords(pwd_file)
        if passwords is None:
            self.log_msg(f'Error: File "{pwd_file}" not found.', "error")
            return
        if len(passwords) == 0:
            self.log_msg("Error: Password file is empty.", "error")
            return

        self.passwords = passwords
        self.running = True
        self.stop_flag = False
        self.found_password = None

        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.result_frame.pack_forget()
        self.result_var.set("")
        self.progress_var.set(0)
        self.progress_text.set("")

        self.clear_log()
        threading.Thread(target=self.run_attack, daemon=True).start()

    def stop_attack(self):
        self.stop_flag = True
        self.status_var.set("Stopping...")

    def run_attack(self):
        host = self.host_var.get().strip()
        port = int(self.port_var.get().strip())
        user = self.user_var.get().strip()
        timeout = int(self.timeout_var.get().strip())
        delay = float(self.delay_var.get().strip())
        total = len(self.passwords)

        self.root.after(0, lambda: self.log_msg(
            f"Target: {host}:{port}   User: {user}   Passwords: {total}", "info"))
        self.root.after(0, lambda: self.log_msg(
            f"File: {self.file_var.get()}", "info"))
        self.root.after(0, lambda: self.log_msg(""))

        self.root.after(0, lambda: self.status_var.set("Connecting..."))
        try:
            tn = telnetlib.Telnet(host, port, timeout=timeout)
            tn.close()
            self.root.after(0, lambda: self.log_msg(
                f"Connection to {host}:{port} successful.", "ok"))
        except Exception as e:
            self.root.after(0, lambda: self.log_msg(
                f"Could not connect to {host}:{port} — {e}", "error"))
            self.root.after(0, lambda: self.status_var.set("Connection failed"))
            self.finish()
            return

        self.root.after(0, lambda: self.log_msg(""))

        for i, pwd in enumerate(self.passwords, 1):
            if self.stop_flag:
                self.root.after(0, lambda: self.log_msg("Stopped by user.", "info"))
                self.root.after(0, lambda: self.status_var.set("Stopped"))
                break

            pct = (i / total) * 100
            self.root.after(0, lambda p=pct: self.progress_var.set(p))
            self.root.after(0, lambda ii=i, pp=pwd: self.status_var.set(
                f"Testing {ii}/{total}: {pp}"))
            self.root.after(0, lambda ii=i, t=total, p=pct: self.progress_text.set(
                f"{ii} / {t}  ({p:.0f}%)"))

            success = self.test_password(host, port, user, pwd, timeout)

            if success:
                self.found_password = pwd
                self.root.after(0, lambda pp=pwd: self.log_msg(
                    f"[{i}/{total}]  {pp}  —  OK", "found"))
                self.root.after(0, lambda: self.log_msg(""))
                self.root.after(0, lambda: self.log_msg(
                    f"Password found!  User: {user}  Password: {pwd}", "found"))
                self.root.after(0, lambda: self.status_var.set("Password found!"))
                self.root.after(0, lambda: self.progress_var.set(100))
                self.root.after(0, lambda: self.result_var.set(
                    f"Password found:  {user} / {pwd}"))
                self.root.after(0, lambda: self.result_label.configure(style="Result.TLabel"))
                self.root.after(0, lambda: self.result_frame.pack(
                    fill="x", pady=(4, 0), before=self.log_group))
                break
            else:
                self.root.after(0, lambda ii=i, pp=pwd: self.log_msg(
                    f"[{ii}/{total}]  {pp}", "fail"))

            time.sleep(delay)
        else:
            if not self.stop_flag:
                self.root.after(0, lambda: self.log_msg(""))
                self.root.after(0, lambda: self.log_msg(
                    "Done — no password matched.", "error"))
                self.root.after(0, lambda: self.status_var.set("Done — no match"))
                self.root.after(0, lambda: self.result_var.set("No password matched"))
                self.root.after(0, lambda: self.result_label.configure(
                    style="ResultFail.TLabel"))
                self.root.after(0, lambda: self.result_frame.pack(
                    fill="x", pady=(4, 0), before=self.log_group))

        self.finish()

    def finish(self):
        self.running = False
        self.root.after(0, lambda: self.start_btn.configure(state="normal"))
        self.root.after(0, lambda: self.stop_btn.configure(state="disabled"))


def main():
    root = tk.Tk()
    app = TelnetCrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
