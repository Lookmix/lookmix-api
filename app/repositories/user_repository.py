from app import db


def save(user):
    id = db['users'].insert_one(user).inserted_id

    return id


def get_by_username(username):
    return db['users'].find_one({'username': username})


def get_by_phone(phone):
    user = db['users'].find_one({'phone': phone})

    if user:
        user['_id'] = str(user['_id'])
    return user


def get_all():
    users = db['users'].find({}, {"password": 0 })

    return list(users)


def update_password(new_password, phone):
    return db['users'].update_one({'phone': phone},
                                     {'$set':
                                          {'password': new_password}
                                      }).modified_count
