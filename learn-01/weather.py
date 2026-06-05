import os
from dotenv import load_dotenv
import requests

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_URL = f"https://api.openweathermap.org/data/3.0/weather?lat=17.3871&lon=78.4916&appid={WEATHER_API_KEY}"

def get_weather():
    response = requests.get(WEATHER_URL)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching weather data: {response.status_code}, {response.text}")
        return None

def main():
    weather_data = get_weather()
    if weather_data:
        print("Weather data fetched successfully:")
        print(weather_data)

if __name__ == "__main__":
    main()