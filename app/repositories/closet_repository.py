from app import db
from bson.objectid import ObjectId

CLOSET_DOC = "closet"
ID_KEY = "_id"
USER_ID = "user_id"
SET_KEY = "$set"

def save(closet):
    id = db[CLOSET_DOC].insert_one(closet).inserted_id
    return id


def get_by_id(id):
    closet = db[CLOSET_DOC].find_one({ID_KEY: id})
    if closet:
        closet[ID_KEY] = str(closet[ID_KEY])
    return closet


def get_by_user_id(id):
	closet = db[CLOSET_DOC].find_one({USER_ID: id})
	if closet:
		closet[ID_KEY] = str(closet[ID_KEY])
	return closet


def update(id, data):
    db[CLOSET_DOC].update_one(
        { ID_KEY:  ObjectId(id) },
        { SET_KEY: data }, upsert=False
    )

