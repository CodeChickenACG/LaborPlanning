import tkinter as tk
from tkinter import ttk
from itertools import cycle, islice
from random import shuffle
import os
import csv
import math

# Function to load CSV into a set of valid logins
def load_permissions(csv_file):
    permissions = set()
    try:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                login = row[1].strip()
                permissions.add(login)
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
    return permissions

# Filter and assign associates based on logins
def filter_and_assign(logins, loads, carts, volume_per_person, permissions_set):
    # Filter valid logins
    valid_logins = [login for login in logins if login in permissions_set]
    invalid_logins = [login for login in logins if login not in permissions_set]

    # Assign associates to loads
    assignments = {}
    valid_logins_pool = valid_logins.copy()

    for load, total_volumes, volume_per_person in zip(loads, carts, volume_per_person):
        shuffle(valid_logins_pool)
        required_assignments = math.ceil(total_volumes / volume_per_person)
        assignments[load] = list(islice(cycle(valid_logins_pool), required_assignments))

    return assignments, invalid_logins

# GUI for the TTB process
def run_ttb_gui():
    permissions_set = load_permissions(r'/backend/Resources\login_name_pair_TTB.csv')

    def process_data():
        logins = login_input.get("1.0", "end").strip().split()
        loads = loads_input.get("1.0", "end").strip().split()
        carts = list(map(int, carts_input.get("1.0", "end").strip().split()))
        carts_per_person = list(map(int, carts_per_person_input.get("1.0", "end").strip().split()))

        assignments, invalid_logins = filter_and_assign(
            logins, loads, carts, carts_per_person, permissions_set
        )

        output_text.delete("1.0", "end")
        output_text.insert("end", "Assignments:\n")
        for load, assigned_logins in assignments.items():
            output_text.insert("end", f"{load}: {' '.join(assigned_logins)}\n")

        output_text.insert("end", "\nInvalid Logins:\n")
        for login in invalid_logins:
            output_text.insert("end", f"{login}\n")

    root = tk.Tk()
    root.title("Associate Assignment Tool - TTB")
    root.geometry("800x600")

    # Input frame
    input_frame = ttk.LabelFrame(root, text="Inputs", padding=(10, 10))
    input_frame.pack(fill="both", expand=True, padx=10, pady=10)

    ttk.Label(input_frame, text="Logins:").grid(row=0, column=0, sticky="w", pady=5)
    login_input = tk.Text(input_frame, height=5, width=50)
    login_input.grid(row=0, column=1, pady=5)

    ttk.Label(input_frame, text="Loads:").grid(row=1, column=0, sticky="w", pady=5)
    loads_input = tk.Text(input_frame, height=2, width=50)
    loads_input.grid(row=1, column=1, pady=5)

    ttk.Label(input_frame, text="Volumes:").grid(row=2, column=0, sticky="w", pady=5)
    carts_input = tk.Text(input_frame, height=2, width=50)
    carts_input.grid(row=2, column=1, pady=5)

    ttk.Label(input_frame, text="Volumes per Person:").grid(row=3, column=0, sticky="w", pady=5)
    carts_per_person_input = tk.Text(input_frame, height=2, width=50)
    carts_per_person_input.grid(row=3, column=1, pady=5)

    process_button = ttk.Button(input_frame, text="Process", command=process_data)
    process_button.grid(row=4, column=1, sticky="e", pady=10)

    # Output frame
    output_frame = ttk.LabelFrame(root, text="Output", padding=(10, 10))
    output_frame.pack(fill="both", expand=True, padx=10, pady=10)

    output_text = tk.Text(output_frame, height=20, width=80, wrap="word")
    output_text.pack(fill="both", expand=True)

    root.mainloop()