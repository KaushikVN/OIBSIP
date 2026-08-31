import sys
import tkinter as tk
from tkinter import messagebox

def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)

def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25.0:
        return "Normal weight"
    elif 25.0 <= bmi < 30.0:
        return "Overweight"
    else:
        return "Obese"

def run_cli():
    print("=======================================")
    print("      OASIS INFOBYTE - BMI CALCULATOR  ")
    print("=======================================")

    while True:
        weight_input = input("\nEnter weight in kg (or 'q' to exit): ").strip()
        if weight_input.lower() == 'q':
            print("Exiting calculator.")
            break
        
        try:
            weight = float(weight_input)
            if weight <= 0:
                print("Error: Weight must be greater than 0.")
                continue
        except ValueError:
            print("Error: Please enter a valid number for weight.")
            continue

        height_input = input("Enter height in meters (e.g., 1.75): ").strip()
        try:
            height = float(height_input)
            if height <= 0:
                print("Error: Height must be greater than 0.")
                continue
        except ValueError:
            print("Error: Please enter a valid number for height.")
            continue

        bmi = calculate_bmi(weight, height)
        category = categorize_bmi(bmi)

        print("---------------------------------------")
        print(f"Calculated BMI : {bmi:.2f}")
        print(f"Category       : {category}")
        print("---------------------------------------")

def run_gui():
    root = tk.Tk()
    root.title("BMI Calculator")
    root.geometry("350x280")
    root.resizable(False, False)

    tk.Label(root, text="BMI Calculator", font=("Arial", 14, "bold")).pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=5)

    tk.Label(frame, text="Weight (kg):", font=("Arial", 10)).grid(row=0, column=0, pady=5, sticky="w")
    weight_entry = tk.Entry(frame, font=("Arial", 10))
    weight_entry.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(frame, text="Height (m):", font=("Arial", 10)).grid(row=1, column=0, pady=5, sticky="w")
    height_entry = tk.Entry(frame, font=("Arial", 10))
    height_entry.grid(row=1, column=1, pady=5, padx=5)

    result_label = tk.Label(root, text="", font=("Arial", 11, "bold"))
    result_label.pack(pady=10)

    def on_calculate():
        try:
            w = float(weight_entry.get().strip())
            h = float(height_entry.get().strip())
            if w <= 0 or h <= 0:
                messagebox.showerror("Invalid Input", "Weight and height must be greater than 0.")
                return
            bmi = calculate_bmi(w, h)
            cat = categorize_bmi(bmi)
            result_label.config(text=f"BMI: {bmi:.2f}\nCategory: {cat}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values.")

    tk.Button(root, text="Calculate", command=on_calculate, font=("Arial", 10, "bold"), bg="#2563eb", fg="white", width=12).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli()
    else:
        try:
            run_gui()
        except Exception:
            run_cli()
