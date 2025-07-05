import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import json

SHORTCUTS_FILE = "shortcuts.json"

def load_shortcuts():
    if os.path.exists(SHORTCUTS_FILE):
        with open(SHORTCUTS_FILE, "r") as f:
            return json.load(f)
    return []

def save_shortcuts(shortcuts):
    with open(SHORTCUTS_FILE, "w") as f:
        json.dump(shortcuts, f)

def add_shortcut():
    name = name_entry.get().strip()
    path = path_entry.get().strip()
    if not name or not path:
        messagebox.showwarning("Input Error", "Both name and path are required.")
        return
    shortcuts.append({"name": name, "path": path})
    save_shortcuts(shortcuts)
    update_listbox()
    name_entry.delete(0, tk.END)
    path_entry.delete(0, tk.END)

def browse_path():
    file_path = filedialog.askopenfilename()
    if file_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, file_path)

def launch_shortcut(event=None):
    selection = listbox.curselection()
    if selection:
        idx = selection[0]
        path = shortcuts[idx]["path"]
        try:
            subprocess.Popen(path, shell=True)
        except Exception as e:
            messagebox.showerror("Launch Error", str(e))

def update_listbox():
    listbox.delete(0, tk.END)
    for s in shortcuts:
        listbox.insert(tk.END, s["name"])

root = tk.Tk()
root.title("Shortcut Creator & Launcher")
root.geometry("400x350")
root.resizable(False, False)

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Input Frame
input_frame = ttk.LabelFrame(main_frame, text="Add New Shortcut", padding="10")
input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

ttk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky="w")
name_entry = ttk.Entry(input_frame, width=30)
name_entry.grid(row=0, column=1, padx=5, pady=2)

ttk.Label(input_frame, text="Path:").grid(row=1, column=0, sticky="w")
path_entry = ttk.Entry(input_frame, width=30)
path_entry.grid(row=1, column=1, padx=5, pady=2)

browse_btn = ttk.Button(input_frame, text="Browse...", command=browse_path)
browse_btn.grid(row=1, column=2, padx=5)

add_btn = ttk.Button(input_frame, text="Add Shortcut", command=add_shortcut)
add_btn.grid(row=2, column=0, columnspan=3, pady=5)

# List Frame
list_frame = ttk.LabelFrame(main_frame, text="Your Shortcuts", padding="10")
list_frame.grid(row=1, column=0, sticky="nsew")

list_frame.rowconfigure(0, weight=1)
list_frame.columnconfigure(0, weight=1)

listbox = tk.Listbox(list_frame, height=10)
listbox.grid(row=0, column=0, sticky="nsew")

scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
listbox.config(yscrollcommand=scrollbar.set)

listbox.bind('<Double-1>', launch_shortcut)

shortcuts = load_shortcuts()
update_listbox()

root.mainloop()