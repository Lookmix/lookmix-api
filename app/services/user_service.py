import flickr_api
import json
from flask import jsonify
from app.services import image_service
from app.repositories import user_repository
from app.utils import validation
from app.exceptions.error import DuplicatedPhoneException, PhoneNotFoundException
from werkzeug.security import generate_password_hash
from bson.json_util import dumps
from datetime import datetime


def save(user):
    try:
        user['timestamp'] = str(datetime.now())

        validate_user_data(user)

        encrypted_password = encrypt_passoword(user['password'])

        user['is_admin'] = False
        user['password'] = encrypted_password

        saved_user = user_repository.save(user)

        return str(saved_user)
    except Exception as e:
        raise e


def get_all():
    try:
        usuarios = user_repository.get_all()

        return dumps(usuarios)
    except Exception as e:
        raise e


def get_by_phone(phone):
    user = user_repository.get_by_phone(phone)

    if user:
        return user
    return None


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
    image_service.set_auth_handler()
    
    return flickr_api.test.login()


def validate_user_data(user):
    validation.assert_valid_schema(user, "user.json")
    
    phone = user['phone']

    if not is_phone_unique(phone):
        raise DuplicatedPhoneException()


def encrypt_passoword(password):
    return generate_password_hash(password)


def is_username_unique(username):
    username = username.lower()

    user = user_repository.get_by_username(username)

    result = True

    if user:
        result = False
    return jsonify({"is_unique": result})


def is_phone_unique(phone):
    user = user_repository.get_by_phone(phone)

    result = True

    if user:
        result = False
    return result


def update_password(password, phone):
    try:
        user = get_by_phone(phone)

        if user:
            encrypted_password = encrypt_passoword(password)

            result = user_repository.update_password(encrypted_password, phone)
            
            return result
        raise PhoneNotFoundException()
    except Exception as e:
        raise e