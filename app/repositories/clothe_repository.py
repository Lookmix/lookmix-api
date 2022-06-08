from app import db
from bson.objectid import ObjectId

CLOTHE_DOC = "clothe"
ID_KEY = "_id"
USER_ID = "user_id"
CLOSET_ID = "closet_id"
SET_KEY = "$set"
PUSH_KEY ="$push"

def save(clothe):
    id = db[CLOTHE_DOC].insert_one(clothe).inserted_id
    return id


def get_by_id(id):
    clothe = db[CLOTHE_DOC].find_one({ID_KEY: ObjectId(id)})
    if clothe:
        clothe[ID_KEY] = str(clothe[ID_KEY])
    return clothe


def get_by_user_id(id):
	clothe = db[CLOTHE_DOC].find_one({USER_ID: ObjectId(id)})
	if clothe:
		clothe[ID_KEY] = str(clothe[ID_KEY])
	return clothe


def update(id, data):
    db[CLOTHE_DOC].update_one(
        { ID_KEY: id },
        { SET_KEY: data }, upsert=False
    )


def get_clothes_by_closet_id(id):
    clothes = db[CLOTHE_DOC].find({CLOSET_ID: id})
    clothes = list(clothes)
    if clothes:
        for c in clothes:
            c[ID_KEY] = str(c[ID_KEY])
    return clothes
