from pymongo import MongoClient
from app.application import application

__mongodb_url = application.config.get("MONGODB_HOST")
__client = MongoClient(__mongodb_url)
db_client = __client["db"]