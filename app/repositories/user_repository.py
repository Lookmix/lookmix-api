from app import db


def save(usuario):
    id = db['usuarios'].insert_one(usuario).inserted_id

    return id


def get_by_username(username):
    return db['usuarios'].find_one({'username': username})


def get_by_phone(phone):
    usuario = db['usuarios'].find_one({'numero_telefone': phone})

    if usuario:
        usuario['_id'] = str(usuario['_id'])
    return usuario


def get_all():
    usuarios = db['usuarios'].find({}, {"password": 0 })

    return list(usuarios)


def update_password(new_password, phone):
    return db['usuarios'].update_one({'numero_telefone': phone},
                                     {'$set':
                                          {'password': new_password}
                                      }).modified_count
