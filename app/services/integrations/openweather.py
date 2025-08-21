from app.application import application
import requests
from datetime import datetime

url = application.config.get("OPEN_WEATHER_URL")
secret = application.config.get("OPEN_WEATHER_SECRET")

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
    daily = data.get("daily")
    daily = sorted(daily, key=lambda day: day["dt"])
    result = []
    for day in daily:
        feels_like = day.get("feels_like")
        result.append(
            {
                "day": feels_like.get("day"),
                "eve": feels_like.get("eve")
            }
        )
    return data


def get_today_weather(lat, long):
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
    today_temp = today.get("feels_like")
    day = today_temp.get("day")
    day = int(day)
    eve = today_temp.get("eve")
    eve = int(eve)
    result = {
        "day": day,
        "eve": eve
    }
    return result