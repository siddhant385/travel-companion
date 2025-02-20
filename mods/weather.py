import requests

# API Keys (Replace with your own keys)
OPENWEATHER_API_KEY = ""
WEATHERAPI_KEY = "db3dc515147c4fa6a6470637252002"
TOMORROW_API_KEY = ""

def get_weather_openweather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "source": "OpenWeather",
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
        }
    return None

def get_weather_weatherapi(city):
    url = f"https://api.weatherapi.com/v1/current.json?key={WEATHERAPI_KEY}&q={city}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return {
            "source": "WeatherAPI",
            "temperature": data["current"]["temp_c"],
            "description": data["current"]["condition"]["text"],
            "humidity": data['current']['humidity'],
            "wind_speed": data['current']['wind_kph']
        }
    return None

def get_weather_tomorrow(city):
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={city}&apikey={TOMORROW_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "source": "Tomorrow.io",
            "temperature": data["data"]["values"]["temperature"],
            "description": "Weather data available",
        }
    return None

def get_weather(city):
    weather_sources = [get_weather_openweather, get_weather_weatherapi, get_weather_tomorrow]
    for source in weather_sources:
        weather = source(city)
        if weather:
            return weather
    return {"error": "No weather data available"}

if __name__ == "__main__":
    weather_info = get_weather_weatherapi("Jabalpur")
    print(weather_info)
