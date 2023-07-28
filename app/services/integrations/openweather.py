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