import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import threading

# Detect SSDs (simplified for demonstration, modify for your system)
def get_drives():
    if os.name == 'nt':  # Windows example
        return ['C:', 'D:']
    else:  # Linux example
        return ['/dev/sda', '/dev/sdb']

# Run secure erase using ATA Secure Erase (Linux Example)
def secure_erase_ssd(drive):
    try:
        # Set a password (required by ATA spec)
        subprocess.run(f"sudo hdparm --user-master u --security-set-pass p {drive}", shell=True, check=True)
        # Perform secure erase
        subprocess.run(f"sudo hdparm --user-master u --security-erase p {drive}", shell=True, check=True)
        messagebox.showinfo("Info", f"Secure erase of {drive} completed!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to securely erase {drive}: {str(e)}")

# GUI Class
class PressurewashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pressurewashr v0.1")

        # Set custom icon
        try:
            self.icon_image = tk.PhotoImage(file="pressurewash.jpg")
            self.root.iconphoto(False, self.icon_image)
        except Exception as e:
            print(f"Failed to load icon: {str(e)}")

        # Drive selection
        self.drive_label = tk.Label(root, text="Select Drive:")
        self.drive_label.pack(pady=10)
        self.drive_list = ttk.Combobox(root, values=get_drives())
        self.drive_list.pack(pady=10)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=20, padx=20, fill='x')

        # Start button for overwriting
        self.start_button = tk.Button(root, text="Start Manual Wipe", command=self.start_wipe)
        self.start_button.pack(pady=10)

        # Secure erase button for SSDs
        self.secure_erase_button = tk.Button(root, text="Secure Erase SSD", command=self.start_secure_erase)
        self.secure_erase_button.pack(pady=10)

    def start_wipe(self):
        selected_drive = self.drive_list.get()
        if not selected_drive:
            messagebox.showerror("Error", "Please select a drive!")
            return
        # Run the wiping process in a new thread to avoid freezing the GUI
        threading.Thread(target=self.wipe_drive, args=(selected_drive,)).start()

    def start_secure_erase(self):
        selected_drive = self.drive_list.get()
        if not selected_drive:
            messagebox.showerror("Error", "Please select a drive!")
            return
        # Perform secure erase in a new thread
        threading.Thread(target=secure_erase_ssd, args=(selected_drive,)).start()

    def wipe_drive(self, drive):
        # Overwriting logic (same as before, modified to handle SSD if needed)
        pass

# Main function to run the app
def main():
    root = tk.Tk()
    app = PressurewashApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
