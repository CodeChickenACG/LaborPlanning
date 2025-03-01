def process_data():
    logins = login_input.get("1.0", "end").strip().split()
    names = name_input.get("1.0", "end").strip().split()
    loads = loads_input.get("1.0", "end").strip().split()
    carts = list(map(int, carts_input.get("1.0", "end").strip().split()))
    carts_per_person = list(map(int, carts_per_person_input.get("1.0", "end").strip().split()))

    assignments, invalid_associates = filter_and_assign(logins, names, loads, carts, carts_per_person)

    # Display results
    output_text.delete("1.0", "end")
    output_text.insert("end", "Assignments:\n")
    for load, assigned_logins in assignments.items():
        output_text.insert("end", f"{load}: {' '.join(assigned_logins)}\n")

    output_text.insert("end", "\nInvalid Associates:\n")
    for login, name in invalid_associates.items():
        output_text.insert("end", f"{login} ({name})\n")