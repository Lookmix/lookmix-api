from pymongo import MongoClient
from app import app

__mongodb_url = app.config.get("MONGODB_HOST")
__client = MongoClient(__mongodb_url)
db_client = __client["db"]