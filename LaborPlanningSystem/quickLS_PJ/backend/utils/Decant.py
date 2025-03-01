import tkinter as tk
from tkinter import filedialog, messagebox

def run_decant_gui():
    def process_decant():
        file_path = filedialog.askopenfilename(title="Select CSV File")
        if not file_path:
            messagebox.showwarning("Warning", "No file selected!")
            return
        # Logic for Decant
        messagebox.showinfo("Info", f"Decant task processed for {file_path}")

    window = tk.Toplevel()
    window.title("Decant")
    window.geometry("300x150")

    tk.Label(window, text="Decant Task", font=("Arial", 14)).pack(pady=10)
    tk.Button(window, text="Select File", command=process_decant, width=20).pack(pady=5)
    tk.Button(window, text="Close", command=window.destroy, width=20).pack(pady=5)

    window.mainloop()
