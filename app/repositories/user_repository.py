from app import db
from bson.objectid import ObjectId

USERS_DOC = "users"
ID_KEY = "_id"

def save(user):
    id = db[USERS_DOC].insert_one(user).inserted_id

    return id


def get_by_id(id):
    user = db[USERS_DOC].find_one({ID_KEY: ObjectId(id)})

    if user:
        user[ID_KEY] = str(user[ID_KEY])
    return user    


def get_by_username(username):
    return db[USERS_DOC].find_one({'username': username})


def get_by_phone(phone):
    user = db[USERS_DOC].find_one({'phone': phone})

    if user:
        user['_id'] = str(user['_id'])
    return user


def get_all():
    users = db[USERS_DOC].find({}, {"password": 0 })

    return list(users)


def update_password(new_password, phone):
    result = db[USERS_DOC].update_one({'phone': phone},
                                     {'$set':
                                          {'password': new_password}
                                      }).modified_count
    return result