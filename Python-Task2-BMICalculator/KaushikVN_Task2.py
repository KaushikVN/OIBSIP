import sys
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Initialize local SQLite database
DB_FILE = "bmi_history.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_record(name, weight, height, bmi, category):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute(
        "INSERT INTO bmi_records (name, weight, height, bmi, category, date) VALUES (?, ?, ?, ?, ?, ?)",
        (name, weight, height, bmi, category, date_str)
    )
    conn.commit()
    conn.close()

def get_user_records(name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT date, bmi FROM bmi_records WHERE LOWER(name) = LOWER(?) ORDER BY id ASC", (name,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)

def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight", "#d97706"
    elif 18.5 <= bmi < 25.0:
        return "Normal weight", "#16a34a"
    elif 25.0 <= bmi < 30.0:
        return "Overweight", "#ea580c"
    else:
        return "Obese", "#dc2626"

def show_trend_graph(name):
    if not name:
        messagebox.showwarning("Notice", "Please enter a user name first.")
        return
    try:
        import matplotlib.pyplot as plt
        records = get_user_records(name)
        if not records or len(records) < 2:
            messagebox.showinfo("Trend Graph", f"Need at least 2 saved records for '{name}' to plot a trend.\nCalculate and save another entry first!")
            return
        
        dates = [r[0] for r in records]
        bmis = [r[1] for r in records]

        plt.figure(figsize=(7, 4.5))
        plt.plot(dates, bmis, marker='o', color='#2563eb', linewidth=2.2, label="Your BMI")
        plt.axhline(18.5, color='#d97706', linestyle='--', label='Underweight (<18.5)')
        plt.axhline(25.0, color='#16a34a', linestyle='--', label='Normal (18.5-24.9)')
        plt.axhline(30.0, color='#dc2626', linestyle='--', label='Obese (>=30.0)')
        
        plt.title(f"BMI History Trend for {name}", fontsize=13, fontweight='bold')
        plt.xlabel("Date & Time")
        plt.ylabel("BMI Value")
        plt.xticks(rotation=25, ha='right')
        plt.legend(loc="upper right", fontsize=8)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.tight_layout()
        plt.show()
    except ImportError:
        messagebox.showerror("Dependency Error", "Please run 'pip install matplotlib' in your terminal.")

def run_gui():
    init_db()
    root = tk.Tk()
    root.title("BMI Calculator Pro - Oasis Infobyte")
    root.geometry("420x460")
    root.resizable(False, False)
    root.configure(bg="#f8fafc")

    tk.Label(root, text="BMI Calculator Pro", font=("Segoe UI", 15, "bold"), bg="#f8fafc", fg="#0f172a").pack(pady=10)

    form = tk.Frame(root, bg="#f8fafc")
    form.pack(pady=5)

    # Inputs
    tk.Label(form, text="User Name:", font=("Segoe UI", 10), bg="#f8fafc").grid(row=0, column=0, sticky="w", pady=4)
    name_entry = tk.Entry(form, font=("Segoe UI", 10), width=18)
    name_entry.grid(row=0, column=1, pady=4, padx=5)
    name_entry.insert(0, "Kaushik")

    tk.Label(form, text="Weight (kg):", font=("Segoe UI", 10), bg="#f8fafc").grid(row=1, column=0, sticky="w", pady=4)
    weight_entry = tk.Entry(form, font=("Segoe UI", 10), width=18)
    weight_entry.grid(row=1, column=1, pady=4, padx=5)
    weight_entry.insert(0, "70")

    tk.Label(form, text="Height (m):", font=("Segoe UI", 10), bg="#f8fafc").grid(row=2, column=0, sticky="w", pady=4)
    height_entry = tk.Entry(form, font=("Segoe UI", 10), width=18)
    height_entry.grid(row=2, column=1, pady=4, padx=5)
    height_entry.insert(0, "1.75")

    # Result Card
    result_card = tk.Label(
        root,
        text="Click 'Calculate & Save' to view BMI",
        font=("Segoe UI", 10, "bold"),
        bg="#ffffff",
        fg="#64748b",
        width=38,
        height=4,
        relief="solid",
        bd=1
    )
    result_card.pack(pady=12)

    def on_calculate():
        name = name_entry.get().strip()
        if not name:
            result_card.config(text="Error: Please enter a user name.", fg="#dc2626")
            return

        try:
            w = float(weight_entry.get().strip())
            h = float(height_entry.get().strip())

            if w <= 0 or h <= 0:
                result_card.config(text="Error: Weight & height must be positive numbers.", fg="#dc2626")
                return

            # Auto-convert cm to meters if user types 175 instead of 1.75
            if h > 3.0:
                h = h / 100.0

            bmi = calculate_bmi(w, h)
            cat, color = categorize_bmi(bmi)

            display_text = f"Calculated BMI: {bmi:.2f}\nClassification: {cat}\nHeight: {h:.2f} m | Weight: {w:.1f} kg"
            result_card.config(text=display_text, fg=color)
            save_record(name, w, h, bmi, cat)

        except ValueError:
            result_card.config(text="Error: Enter valid numerical values.", fg="#dc2626")

    # Buttons
    btn_frame = tk.Frame(root, bg="#f8fafc")
    btn_frame.pack(pady=6)

    tk.Button(btn_frame, text="Calculate & Save", command=on_calculate, bg="#2563eb", fg="white", font=("Segoe UI", 10, "bold"), width=16, relief="flat", cursor="hand2").grid(row=0, column=0, padx=4)
    tk.Button(btn_frame, text="View Trend Graph", command=lambda: show_trend_graph(name_entry.get().strip()), bg="#0f766e", fg="white", font=("Segoe UI", 10, "bold"), width=16, relief="flat", cursor="hand2").grid(row=0, column=1, padx=4)

    root.mainloop()

if __name__ == "__main__":
    run_gui()