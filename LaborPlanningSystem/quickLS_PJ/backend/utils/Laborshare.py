import tkinter as tk
from tkinter import filedialog, messagebox

def run_laborshare_gui():
    def process_file():
        file_path = filedialog.askopenfilename(title="Select CSV File")
        if not file_path:
            messagebox.showwarning("Warning", "No file selected!")
            return
        # Logic for processing the file
        messagebox.showinfo("Info", f"Laborshare processed for {file_path}")

    window = tk.Toplevel()
    window.title("Laborshare")
    window.geometry("300x150")

    tk.Label(window, text="Laborshare Task", font=("Arial", 14)).pack(pady=10)
    tk.Button(window, text="Select File", command=process_file, width=20).pack(pady=5)
    tk.Button(window, text="Close", command=window.destroy, width=20).pack(pady=5)

    window.mainloop()
