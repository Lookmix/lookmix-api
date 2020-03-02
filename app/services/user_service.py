import flickr_api
import json
from flask import jsonify
from app.services import flickr_service
from app.repositories import user_repository
from app.utils import validation
from app.exceptions.error import TelefoneDuplicadoException, UsernameDuplicadoException
from werkzeug.security import generate_password_hash
from bson.json_util import dumps


def save(user):
    try:
        validate_user_data(user)

        encrypted_password = encrypt_passoword(user['password'])

        user['is_admin'] = False
        user['password'] = encrypted_password

        return dumps(user_repository.save(user))
    except Exception as e:
        raise e


def get_all():
    try:
        usuarios = user_repository.get_all()

        return dumps(usuarios)
    except Exception as e:
        raise e


def get_photos():
    user = get_user_flickr()
    photos = user.getPhotos()
    photos_data = photos.data
    photos_list_json = []

    for photo in photos_data:
        default = lambda o: f"<<non-serializable: {type(o).__qualname__}>>"
        photo_json = json.dumps(photo.__dict__, default=default)
        photos_list_json.append(json.loads(photo_json))
    return photos_list_json


def get_user_flickr():
    flickr_service.set_auth_handler()
    
    return flickr_api.test.login()


def validate_user_data(user):
    validation.assert_valid_schema(user, "usuario.json")

    if not validation.is_phone_unique(user['numero_telefone']):
        raise TelefoneDuplicadoException()
    
    if not validation.is_username_unique(user['username']):
        raise UsernameDuplicadoException()


def encrypt_passoword(password):
    return generate_password_hash(password)


def is_username_unique(username):
    return jsonify({"is_unique": validation.is_username_unique(username)})


def is_phone_unique(phone):
    return jsonify({"is_unique": validation.is_phone_unique(phone)})