import sys
import requests
import tkinter as tk
from tkinter import messagebox

API_KEY = "bd5e378503939ddaee76f12ad7a97608"

def fetch_weather(city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        temp_c = data["main"]["temp"]
        temp_f = (temp_c * 9/5) + 32
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp_c": temp_c,
            "temp_f": temp_f,
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].title(),
            "wind_speed": data["wind"]["speed"]
        }
    elif response.status_code == 404:
        raise ValueError("City not found. Please verify the name.")
    else:
        raise ConnectionError(f"API Error: {response.status_code}")

def run_cli():
    print("=======================================")
    print("      OASIS INFOBYTE - WEATHER APP     ")
    print("=======================================")

    while True:
        city = input("\nEnter city name (or 'q' to quit): ").strip()
        if city.lower() == 'q':
            print("Exiting weather app.")
            break
        if not city:
            print("Error: City name cannot be empty.")
            continue

        try:
            w = fetch_weather(city)
            print("---------------------------------------")
            print(f"Location    : {w['city']}, {w['country']}")
            print(f"Condition   : {w['description']}")
            print(f"Temperature : {w['temp_c']:.1f}°C / {w['temp_f']:.1f}°F")
            print(f"Humidity    : {w['humidity']}%")
            print(f"Wind Speed  : {w['wind_speed']} m/s")
            print("---------------------------------------")
        except Exception as e:
            print(f"Error: {e}")

def run_gui():
    root = tk.Tk()
    root.title("Weather App - Oasis Infobyte")
    root.geometry("380x360")
    root.resizable(False, False)
    root.configure(bg="#f1f5f9")

    tk.Label(root, text="Weather App", font=("Arial", 14, "bold"), bg="#f1f5f9", fg="#0f172a").pack(pady=10)

    frame = tk.Frame(root, bg="#f1f5f9")
    frame.pack(pady=5)

    city_entry = tk.Entry(frame, font=("Arial", 11), width=18)
    city_entry.grid(row=0, column=0, padx=5)
    city_entry.focus()

    res_card = tk.Label(root, text="Enter a city to get weather details", font=("Arial", 10), bg="#ffffff", fg="#334155", width=34, height=8, relief="solid", bd=1)
    res_card.pack(pady=15)

    def on_search():
        city = city_entry.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name.")
            return
        try:
            w = fetch_weather(city)
            text = (
                f"Location: {w['city']}, {w['country']}\n\n"
                f"Condition: {w['description']}\n"
                f"Temperature: {w['temp_c']:.1f}°C ({w['temp_f']:.1f}°F)\n"
                f"Humidity: {w['humidity']}%\n"
                f"Wind Speed: {w['wind_speed']} m/s"
            )
            res_card.config(text=text, justify="left")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frame, text="Search", command=on_search, bg="#0284c7", fg="white", font=("Arial", 10, "bold"), width=8).grid(row=0, column=1, padx=5)

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli()
    else:
        try:
            run_gui()
        except Exception:
            run_cli()