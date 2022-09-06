from app import db
from bson.objectid import ObjectId


CLOTHE_COLLECTION = "clothe"
ID_KEY = "_id"
USER_ID_KEY = "user_id"
CLOSET_ID_KEY = "closet_id"
TYPE_KEY = "type"
SET_KEY = "$set"
PUSH_KEY = "$push"
IN_KEY = "$in"
SOCIAL_TYPE = "social"
CASUAL_TYPE = "casual"

def save(clothe):
    id = db[CLOTHE_COLLECTION].insert_one(clothe).inserted_id
    return id


def get_by_id(id):
    clothe = db[CLOTHE_COLLECTION].find_one({ID_KEY: ObjectId(id)})
    if clothe:
        clothe[ID_KEY] = str(clothe[ID_KEY])
    return clothe


def get_by_user_id(id):
	clothe = db[CLOTHE_COLLECTION].find_one({USER_ID_KEY: ObjectId(id)})
	if clothe:
		clothe[ID_KEY] = str(clothe[ID_KEY])
	return clothe


def update_by_id(id, data):
    del data["_id"]
    result = db[CLOTHE_COLLECTION].update_one(
        { ID_KEY: ObjectId(id) },
        { SET_KEY: data }
    )
    return result


def get_clothes_by_closet_id(id):
    clothes = db[CLOTHE_COLLECTION].find({CLOSET_ID_KEY: id})
    clothes = list(clothes)
    if clothes:
        for c in clothes:
            c[ID_KEY] = str(c[ID_KEY])
    return clothes


def get_social_clothes_by_closet_id(id):
    clothes = db[CLOTHE_COLLECTION].find({
        CLOSET_ID_KEY: id,
        TYPE_KEY: SOCIAL_TYPE
    })
    clothes = list(clothes)
    if clothes:
        for c in clothes:
            c[ID_KEY] = str(c[ID_KEY])
    return clothes


def get_casual_clothes_by_closet_id(id):
    clothes = db[CLOTHE_COLLECTION].find({
        CLOSET_ID_KEY: id,
        TYPE_KEY: CASUAL_TYPE
    })
    clothes = list(clothes)
    if clothes:
        for c in clothes:
            c[ID_KEY] = str(c[ID_KEY])
    return clothes


def delete_by_ids (ids):
    ids = [ObjectId(id) for id in ids]

    result = db[CLOTHE_COLLECTION].delete_many({
        ID_KEY: { IN_KEY: ids }
    })
    return result


def update_clothe_occasions():
    occasions_result = db["occasion"].find({})
    occasions = list(occasions_result)
    occasions = { occasion["name"]: str(occasion["_id"]) for occasion in occasions }
    clothes_result = db["clotheii"].find({})
    clothes = list(clothes_result)
    for clothe in clothes:
        clothe_occasions = clothe["occasions"]
        for index, clothe_occasion in enumerate(clothe_occasions):
            clothe_occasion_lower = clothe_occasion.lower()
            id = occasions[clothe_occasion_lower]
            clothe["occasions"][index] = id
        clothe_id = clothe["_id"]
        db["clotheii"].update_one(
            { ID_KEY: clothe_id },
            { SET_KEY: { "occasions": clothe["occasions"] } }
        )
