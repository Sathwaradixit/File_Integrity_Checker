import hashlib
import os
import time
import threading 
import tkinter as tk
from tkinter import filedialog, messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Calculate hash file
def cal_hash(fpath, hashalgo='sha256'):
    try:
        hashfunc = hashlib.new(hashalgo)
        with open(fpath, 'rb') as f:
            while chunk := f.read(8192):
                hashfunc.update(chunk)
        return hashfunc.hexdigest()
    except FileNotFoundError:
        return None
    except Exception as e:
        return str(e)

# Check file integrity by comparing hashes
def check_integrity(fpath, khash, hashalgo='sha256'):
    curhash = cal_hash(fpath, hashalgo)
    if curhash is None:
        return False, "File not found or Calculating hash"
    if curhash == khash:
        return True, "File integrity check passed!"
    else:
        return False, "File integrity check failed!"
    
# Using watchdog monitor file changes
class FChangeHand(FileSystemEventHandler):
    def __init__(self, fpath):
        self.fpath = fpath
        self.prehash = cal_hash(self.fpath)

    def on_modified(self, event):
        if event.src_path == self.fpath:
            curhash = cal_hash(self.fpath)
            if curhash != self.prehash:
                print(f"File {self.fpath} has been modified...")
                self.prehash = curhash
            else:
                print(f"File {self.fpath} has not changed.")

# Start monitoring file
def fmon(fpath):
    event_hand = FChangeHand(fpath)
    obs = Observer()    
    obs.schedule(event_hand, path=os.path.dirname(fpath), recursive=False)
    obs.start()
    print(f"Started monitoring: {fpath}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
    obs.join()                            

# GUI base file integrity checker and monitoring    
class FileIntegrityCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Integrity Checker")
        self.root.geometry("500x400")

        self.fpath = None
        self.prehash = None

        # Browse File
        self.flable = tk.Label(self.root, text="Select file to check:")
        self.flable.pack(pady=5)
        self.fbtn = tk.Button(self.root, text="Browse", command=self.fselect)
        self.fbtn.pack(pady=10)

        # Entry of Known Hash
        self.khash_label = tk.Label(self.root, text="Enter known hash:")
        self.khash_label.pack(pady=5)
        self.khash_entry = tk.Entry(self.root, width=30)
        self.khash_entry.pack(pady=5)

        # Select hash algorithm
        self.hashalgo_label = tk.Label(self.root, text="Select hash algorithm:")
        self.hashalgo_label.pack(pady=5)
        self.hashalgo_var = tk.StringVar(value="sha256")
        self.hashalgo_menu = tk.OptionMenu(self.root, self.hashalgo_var, "sha256", "md5", "sha1", "sha512")
        self.hashalgo_menu.pack(pady=5)

        # Check integrity button
        self.check_integrity_btn = tk.Button(self.root, text="Check Integrity", command=self.check_integrity)
        self.check_integrity_btn.pack(pady=10)

        # Display result
        self.res_label = tk.Label(self.root, text="")
        self.res_label.pack(pady=20)

        # Monitoring Status
        self.mon_label = tk.Label(self.root, text="Not monitoring any file.") 
        self.mon_label.pack(pady=5)

    def fselect(self):
        self.fpath = filedialog.askopenfilename()
        if self.fpath:
            self.res_label.config(text=f"Selected file: {self.fpath}")

    def check_integrity(self):
        if not self.fpath:
            messagebox.showerror("Error", "No file selected.")
            return

        khash = self.khash_entry.get()
        if not khash:
            messagebox.showerror("Error", "Please enter the known hash.")
            return

        hashalgo = self.hashalgo_var.get()

        valid, message = check_integrity(self.fpath, khash, hashalgo)
        self.res_label.config(text=message)

        # Change text color based on the result
        if valid:
            self.res_label.config(fg="green")  # Set text color to green if integrity check passes
            self.prehash = cal_hash(self.fpath, hashalgo)
            self.mon_label.config(text=f"Monitoring file: {os.path.basename(self.fpath)}")
            threading.Thread(target=fmon, args=(self.fpath,), daemon=True).start()
        else:
            self.res_label.config(fg="red")  # Set text color to red if integrity check fails

# Create and Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = FileIntegrityCheckerApp(root)
    root.mainloop()