from app import db
from bson.objectid import ObjectId

DAILY_LOOK_SETUP_COLLECTION = "daily_look_setup"
LOOKSET_COLLECTION = "lookset"
ID_KEY = "_id"
USER_ID_KEY = "user_id"
SET_KEY = "$set"
PUSH_KEY = "$push"
IN_KEY = "$in"


def update_daily_look_setup(user_id, data):
	result = db[DAILY_LOOK_SETUP_COLLECTION].update_one(
		{ USER_ID_KEY: user_id },
		{ SET_KEY: data },
		upsert=True
	).modified_count
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

def save_look(data):
    id = db[LOOKSET_COLLECTION].insert_one(data).inserted_id
    return id

def save_lookset(data, user_id):
    ids = db[LOOKSET_COLLECTION].update_one(
		{ USER_ID_KEY: user_id },
		{ SET_KEY: data },
		upsert=True
	).modified_count
    return ids

def get_look_set(user_id, timestamp=None, type=None, occasion=None):
	lookset = db[LOOKSET_COLLECTION].aggregate([
		{ "$match": { USER_ID_KEY: user_id } },
		{ 
			"$project": {
				"user_id": 1,
				"looks": {
					"$filter": {
						"input": "$looks",
						"as": "item",
						"cond": { "$eq": [ "$$item.type", type ] }
					}
				}
			} 
		}
	])
	lookset = list(lookset)
	if len(lookset) == 1:
		lookset = lookset[0]
		lookset[ID_KEY] = str(lookset[ID_KEY])
	return lookset

def update_lookset_casual(user_id, data):
	result = db[LOOKSET_COLLECTION].update_one(
		{ USER_ID_KEY: user_id },
		{ SET_KEY: { "casual": data } }
	).modified_count
	return result

def update_lookset_social(user_id, data):
	result = db[LOOKSET_COLLECTION].update_one(
		{ USER_ID_KEY: user_id },
		{ SET_KEY: { "social": data } }
	).modified_count
	return result