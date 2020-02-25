from app import db


def save(usuario):
    id = db['usuarios'].insert_one(usuario).inserted_id

    return id


def get_by_username(username):
    return db['usuarios'].find_one({'username': username})


def get_by_phone(phone):
    return db['usuarios'].find_one({'numero_telefone': phone})


def get_all():
    usuarios = db['usuarios'].find({}, {"password": 0 })

    return list(usuarios)
