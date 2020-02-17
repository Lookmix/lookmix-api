from app import db


def save(usuario):
    id = db['usuarios'].insert_one(usuario).inserted_id

    return id


def get_all():
    usuarios = db['usuarios'].find({}, {"password": 0 })

    return list(usuarios)
