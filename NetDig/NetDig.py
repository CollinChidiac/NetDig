import subprocess
import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import tempfile
from datetime import datetime
import ctypes
import sys

# --- Admin Rights Check ---
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    messagebox.showerror("Admin Required", "You must run this application as an administrator.")
    sys.exit()

# --- Logging Setup ---
log_dir = tempfile.gettempdir()
log_file = os.path.join(log_dir, f"netdig_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

def log_output(command, output):
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"Command: {command}\n")
        f.write(f"Output:\n{output}\n")
        f.write("="*60 + "\n")

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout if result.returncode == 0 else result.stderr
        log_output(command, output)
        if result.returncode != 0:
            raise Exception(output)
        return output
    except Exception as e:
        log_output(command, str(e))
        messagebox.showerror("Error Running Command", str(e))
        return ""

def get_user_input(prompt="Enter the username:"):
    return simpledialog.askstring("Input", prompt)

def show_result(title, result):
    if result:
        messagebox.showinfo(title, result)

def user_domain_info():
    username = get_user_input()
    if username:
        result = run_command(f'net user "{username}" /domain')
        show_result("User Domain Info", result)

def account_info():
    username = get_user_input()
    if username:
        result = run_command(f'net user "{username}"')
        show_result("Account Info", result)

def change_password():
    username = get_user_input()
    if username:
        password = simpledialog.askstring("Password", f"Enter new password for {username}:", show='*')
        if password:
            result = run_command(f'net user "{username}" "{password}"')
            show_result("Change Password", result)

def force_gpupdate():
    result = run_command("gpupdate /force")
    show_result("GPUpdate Result", result)

def net_user_general():
    result = run_command("net user")
    show_result("All Users", result)

# --- GUI Setup ---
root = tk.Tk()
root.title("NetDig - AD Toolkit")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="NetDig - AD User Toolkit", font=("Segoe UI", 14, "bold")).pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10, padx=20)

btn_config = {
    "padx": 10,
    "pady": 5,
    "fill": 'x',
    "expand": True,
}

tk.Button(button_frame, text="User Domain Info", command=user_domain_info).pack(**btn_config)
tk.Button(button_frame, text="Account Info", command=account_info).pack(**btn_config)
tk.Button(button_frame, text="Change Password", command=change_password).pack(**btn_config)
tk.Button(button_frame, text="Force GPUpdate", command=force_gpupdate).pack(**btn_config)
tk.Button(button_frame, text="List All Users", command=net_user_general).pack(**btn_config)

tk.Label(root, text=f"Logging to: {log_file}", font=("Segoe UI", 8)).pack(side='bottom', pady=5)

root.mainloop()
