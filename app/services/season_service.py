from app.repositories import enum_repository
from app.services.integrations import openweather

def get_seasons():
    try:
        seasons = enum_repository.get_seasons()
        return seasons
    except Exception as e:
        raise e


def get_week_weather(lat, long):
    try:
        data = openweather.get_week_weather(lat, long)
        return data
    except Exception as e:
        raise e
    
def get_daily_min_and_max_temperatures(lat, long):
    try:
        data = openweather.get_daily_weather(lat, long)
        return data
    except Exception as e:
        raise e