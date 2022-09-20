from app import db
from bson.objectid import ObjectId

DAILY_LOOK_SETUP_COLLECTION = "daily_look_setup"
ID_KEY = "_id"
USER_ID_KEY = "user_id"
SET_KEY = "$set"
PUSH_KEY = "$push"
IN_KEY = "$in"

def save_daily_look_setup(data):
	id = db[DAILY_LOOK_SETUP_COLLECTION].insert_one(data).inserted_id
	return str(id)

def update_daily_look_setup(user_id, data):
	result = db[DAILY_LOOK_SETUP_COLLECTION].update_one(
		{ USER_ID_KEY: user_id },
		{ SET_KEY: data },
		upsert=True
	)
	return result

def get_daily_look_setup_by_id(id):
    daily_look_setup = db[DAILY_LOOK_SETUP_COLLECTION].find_one(
		{ ID_KEY: ObjectId(id) }
	)
    if daily_look_setup:
        daily_look_setup[ID_KEY] = str(daily_look_setup[ID_KEY])
    return daily_look_setup

def get_daily_look_setup_by_user_id(id):
	daily_look_setup = db[DAILY_LOOK_SETUP_COLLECTION].find_one(
		{ USER_ID_KEY: id }
	)
	if daily_look_setup:
		daily_look_setup[ID_KEY] = str(daily_look_setup[ID_KEY])
	return daily_look_setup