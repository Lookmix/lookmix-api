from app import db
from bson.objectid import ObjectId

CLOSET_COLLECTION = "closet"
ID_KEY = "_id"
USER_ID = "user_id"
SET_KEY = "$set"

def save(closet):
    id = db[CLOSET_COLLECTION].insert_one(closet).inserted_id
    return id


def get_by_id(id):
    closet = db[CLOSET_COLLECTION].find_one({ID_KEY: id})
    if closet:
        closet[ID_KEY] = str(closet[ID_KEY])
    return closet


def get_by_user_id(id):
	closet = db[CLOSET_COLLECTION].find_one({USER_ID: id})
	if closet:
		closet[ID_KEY] = str(closet[ID_KEY])
	return closet


def update(id, data):
    db[CLOSET_COLLECTION].update_one(
        { ID_KEY:  ObjectId(id) },
        { SET_KEY: data }, upsert=False
    )

