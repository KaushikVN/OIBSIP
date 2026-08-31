import sys
import secrets
import string
import tkinter as tk
from tkinter import messagebox

def generate_password(length, use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous=False):
    chars = ""
    guaranteed = []

    upper_set = string.ascii_uppercase
    lower_set = string.ascii_lowercase
    digit_set = string.digits
    symbol_set = string.punctuation

    if exclude_ambiguous:
        ambiguous = "l1I0O"
        upper_set = "".join(c for c in upper_set if c not in ambiguous)
        lower_set = "".join(c for c in lower_set if c not in ambiguous)
        digit_set = "".join(c for c in digit_set if c not in ambiguous)
        symbol_set = "".join(c for c in symbol_set if c not in ambiguous)

    if use_upper:
        chars += upper_set
        guaranteed.append(secrets.choice(upper_set))
    if use_lower:
        chars += lower_set
        guaranteed.append(secrets.choice(lower_set))
    if use_digits:
        chars += digit_set
        guaranteed.append(secrets.choice(digit_set))
    if use_symbols:
        chars += symbol_set
        guaranteed.append(secrets.choice(symbol_set))

    if not chars:
        raise ValueError("At least one character type must be selected.")

    if length < len(guaranteed):
        raise ValueError(f"Password length must be at least {len(guaranteed)}.")

    remaining_length = length - len(guaranteed)
    remaining_chars = [secrets.choice(chars) for _ in range(remaining_length)]
    
    password_list = guaranteed + remaining_chars
    secrets.SystemRandom().shuffle(password_list)
    return "".join(password_list)

def calculate_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    types_count = sum([has_upper, has_lower, has_digit, has_symbol])

    if length >= 12 and types_count >= 3:
        return "Strong", "#16a34a"
    elif length >= 8 and types_count >= 2:
        return "Medium", "#ea580c"
    else:
        return "Weak", "#dc2626"

def run_cli():
    print("=======================================")
    print("   OASIS INFOBYTE - PASSWORD GENERATOR ")
    print("=======================================")

    while True:
        len_input = input("\nEnter password length (minimum 8, or 'q' to quit): ").strip()
        if len_input.lower() == 'q':
            print("Exiting password generator.")
            break
        
        try:
            length = int(len_input)
            if length < 8:
                print("Error: Length must be at least 8 characters.")
                continue
        except ValueError:
            print("Error: Please enter a valid integer number.")
            continue

        print("\nSelect character types to include (y/n):")
        u = input("Include Uppercase letters (A-Z)? [y/n]: ").strip().lower() == 'y'
        l = input("Include Lowercase letters (a-z)? [y/n]: ").strip().lower() == 'y'
        d = input("Include Numbers (0-9)? [y/n]: ").strip().lower() == 'y'
        s = input("Include Symbols (!@#$...)? [y/n]: ").strip().lower() == 'y'

        if not any([u, l, d, s]):
            print("Error: You must select at least one character type.")
            continue

        pwd = generate_password(length, u, l, d, s)
        strength, _ = calculate_strength(pwd)

        print("---------------------------------------")
        print(f"Generated Password : {pwd}")
        print(f"Password Strength  : {strength}")
        print("---------------------------------------")

def run_gui():
    root = tk.Tk()
    root.title("Password Generator - Oasis Infobyte")
    root.geometry("400x420")
    root.resizable(False, False)
    root.configure(bg="#f8fafc")

    tk.Label(root, text="Password Generator", font=("Arial", 14, "bold"), bg="#f8fafc", fg="#0f172a").pack(pady=10)

    frame = tk.Frame(root, bg="#f8fafc")
    frame.pack(pady=5)

    tk.Label(frame, text="Password Length (min 8):", font=("Arial", 10), bg="#f8fafc").grid(row=0, column=0, sticky="w", pady=5)
    length_spin = tk.Spinbox(frame, from_=8, to=64, width=8, font=("Arial", 10))
    length_spin.delete(0, "end")
    length_spin.insert(0, "12")
    length_spin.grid(row=0, column=1, pady=5, padx=5)

    var_upper = tk.BooleanVar(value=True)
    var_lower = tk.BooleanVar(value=True)
    var_digits = tk.BooleanVar(value=True)
    var_symbols = tk.BooleanVar(value=True)
    var_ambig = tk.BooleanVar(value=False)

    tk.Checkbutton(frame, text="Include Uppercase Letters (A-Z)", variable=var_upper, bg="#f8fafc").grid(row=1, column=0, columnspan=2, sticky="w")
    tk.Checkbutton(frame, text="Include Lowercase Letters (a-z)", variable=var_lower, bg="#f8fafc").grid(row=2, column=0, columnspan=2, sticky="w")
    tk.Checkbutton(frame, text="Include Digits (0-9)", variable=var_digits, bg="#f8fafc").grid(row=3, column=0, columnspan=2, sticky="w")
    tk.Checkbutton(frame, text="Include Symbols (!@#$)", variable=var_symbols, bg="#f8fafc").grid(row=4, column=0, columnspan=2, sticky="w")
    tk.Checkbutton(frame, text="Exclude Ambiguous Characters (0, O, 1, l)", variable=var_ambig, bg="#f8fafc").grid(row=5, column=0, columnspan=2, sticky="w")

    pwd_entry = tk.Entry(root, font=("Consolas", 12), width=28, justify="center")
    pwd_entry.pack(pady=10)

    strength_label = tk.Label(root, text="", font=("Arial", 10, "bold"), bg="#f8fafc")
    strength_label.pack(pady=2)

    def on_generate():
        try:
            length = int(length_spin.get().strip())
            pwd = generate_password(
                length,
                var_upper.get(),
                var_lower.get(),
                var_digits.get(),
                var_symbols.get(),
                var_ambig.get()
            )
            pwd_entry.delete(0, tk.END)
            pwd_entry.insert(0, pwd)

            strength, color = calculate_strength(pwd)
            strength_label.config(text=f"Strength: {strength}", fg=color)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copy_to_clipboard():
        pwd = pwd_entry.get().strip()
        if pwd:
            root.clipboard_clear()
            root.clipboard_append(pwd)
            messagebox.showinfo("Copied", "Password copied to clipboard!")

    btn_frame = tk.Frame(root, bg="#f8fafc")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Generate", command=on_generate, bg="#2563eb", fg="white", font=("Arial", 10, "bold"), width=12).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Copy", command=copy_to_clipboard, bg="#475569", fg="white", font=("Arial", 10, "bold"), width=10).grid(row=0, column=1, padx=5)

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli()
    else:
        try:
            run_gui()
        except Exception:
            run_cli()