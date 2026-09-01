import sys
import requests
import tkinter as tk
from tkinter import messagebox

# WMO Weather interpretation codes
WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
}

def fetch_weather(city_name):
    # Step 1: Geocode city name to lat/lon
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    geo_res = requests.get(geo_url, timeout=10)
    
    if geo_res.status_code != 200:
        raise ConnectionError("Network error while resolving city location.")
    
    geo_data = geo_res.json()
    if not geo_data.get("results"):
        raise ValueError(f"City '{city_name}' not found. Please check the spelling.")
    
    location = geo_data["results"][0]
    lat = location["latitude"]
    lon = location["longitude"]
    resolved_name = location.get("name", city_name)
    country = location.get("country", "")

    # Step 2: Fetch current weather metrics
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
    )
    weather_res = requests.get(weather_url, timeout=10)
    if weather_res.status_code != 200:
        raise ConnectionError("Failed to retrieve weather data.")
    
    w_data = weather_res.json().get("current", {})
    temp_c = w_data.get("temperature_2m", 0.0)
    temp_f = (temp_c * 9/5) + 32
    humidity = w_data.get("relative_humidity_2m", 0)
    wind_speed = w_data.get("wind_speed_10m", 0.0)
    weather_code = w_data.get("weather_code", 0)
    description = WMO_CODES.get(weather_code, "Partly Cloudy")

    return {
        "city": resolved_name,
        "country": country,
        "temp_c": temp_c,
        "temp_f": temp_f,
        "humidity": humidity,
        "description": description,
        "wind_speed": wind_speed
    }

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
            print(f"Wind Speed  : {w['wind_speed']} km/h")
            print("---------------------------------------")
        except Exception as e:
            print(f"Error: {e}")

def run_gui():
    root = tk.Tk()
    root.title("Weather App - Oasis Infobyte")
    root.geometry("400x380")
    root.resizable(False, False)
    root.configure(bg="#f8fafc")

    tk.Label(root, text="Weather App", font=("Segoe UI", 15, "bold"), bg="#f8fafc", fg="#0f172a").pack(pady=12)

    frame = tk.Frame(root, bg="#f8fafc")
    frame.pack(pady=6)

    city_entry = tk.Entry(frame, font=("Segoe UI", 11), width=18)
    city_entry.grid(row=0, column=0, padx=5)
    city_entry.insert(0, "Bengaluru")
    city_entry.focus()

    res_card = tk.Label(
        root,
        text="Enter a city and click Search",
        font=("Segoe UI", 10),
        bg="#ffffff",
        fg="#475569",
        width=36,
        height=8,
        relief="solid",
        bd=1,
        justify="left",
        padx=10,
        pady=8
    )
    res_card.pack(pady=15)

    def on_search():
        city = city_entry.get().strip()
        if not city:
            res_card.config(text="Error: Please enter a city name.", fg="#dc2626")
            return
        try:
            w = fetch_weather(city)
            text = (
                f"📍 Location    : {w['city']}, {w['country']}\n"
                f"☁️ Condition   : {w['description']}\n"
                f"🌡️ Temperature : {w['temp_c']:.1f}°C ({w['temp_f']:.1f}°F)\n"
                f"💧 Humidity    : {w['humidity']}%\n"
                f"💨 Wind Speed  : {w['wind_speed']} km/h"
            )
            res_card.config(text=text, fg="#0f172a")
        except Exception as e:
            res_card.config(text=f"Error: {e}", fg="#dc2626")

    tk.Button(
        frame,
        text="Search",
        command=on_search,
        bg="#0284c7",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        width=8,
        relief="flat",
        cursor="hand2"
    ).grid(row=0, column=1, padx=5)

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli()
    else:
        try:
            run_gui()
        except Exception:
            run_cli()