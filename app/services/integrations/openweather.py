from app import app
import requests
from datetime import datetime

url = app.config.get("OPEN_WEATHER_URL")
secret = app.config.get("OPEN_WEATHER_SECRET")

# https://openweathermap.org/api/one-call-3#data
# https://openweathermap.org/api/geocoding-api
def get_week_weather (lat, long):
    global url
    global secret
    response = requests.get(url=url, params={
        "lat": lat,
        "lon": long,
        "exclude": "alerts,minutely,hourly,current",
        "appid": secret,
        "units": "metric" # celsius
    })
    data = response.json()
    # daily = data["daily"]
    # for day in daily:
        # day["dt"] = datetime.fromtimestamp(day["dt"])
        # datetime.date(datetime)
    # data["daily"] = daily
    return data


def get_daily_weather(lat, long):
    global url
    global secret
    response = requests.get(url=url, params={
        "lat": lat,
        "lon": long,
        "exclude": "alerts,minutely,hourly,current",
        "appid": secret,
        "units": "metric" # celsius
    })
    data = response.json()
    data = data.get("daily")
    data = sorted(data, key=lambda day: day["dt"])
    today = data[0]
    today_temp = today.get("temp")
    min = today_temp.get("min")
    min = int(min)
    max = today_temp.get("max")
    max = int(max)
    result = {
        "min": min,
        "max": max
    }
    return result