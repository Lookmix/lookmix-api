import flickr_api
import json
from flask import jsonify
from app.services import image_service
from app.repositories import user_repository
from app.utils import validation
from app.exceptions.error import (
    DuplicatedPhoneException, 
    PhoneNotFoundException,
    EmailNotFoundException,
    DuplicatedEmailException
)
from werkzeug.security import generate_password_hash
from bson.json_util import dumps
from datetime import datetime


def save(user):
    try:
        user["timestamp"] = str(datetime.now()) # TODO: rename to created_at
        # lat = user["lat"]
        # long = user["long"]
        validate_user_data(user)
        encrypted_password = encrypt_passoword(user['password'])
        user["is_admin"] = False # TODO: delete this
        user["password"] = encrypted_password
        saved_user = user_repository.save(user)
        return str(saved_user)
    except Exception as e:
        raise e


# uses email instead of phone
def save2(user):
    try:
        user["timestamp"] = str(datetime.now()) # TODO: rename to created_at
        # lat = user["lat"]
        # long = user["long"]
        validate_user_data2(user)
        encrypted_password = encrypt_passoword(user['password'])
        user["password"] = encrypted_password
        saved_user = user_repository.save(user)
        return str(saved_user)
    except Exception as e:
        raise e


def update_user(user):
    pass


def get_by_id(id):
    user = user_repository.get_by_id(id)

    if user:
        return user
    return None


def get_all():
    try:
        users = user_repository.get_all()

        return dumps(users)
    except Exception as e:
        raise e


def get_by_phone(phone):
    user = user_repository.get_by_phone(phone)

    if user:
        return user
    return None


def get_by_email(email):
    user = user_repository.get_by_email(email)
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


# uses email instead of phone
def validate_user_data2(user):
    validation.assert_valid_schema(user, "user.json")
    email = user['email']
    if not is_email_unique(email):
        raise DuplicatedEmailException()

def encrypt_passoword(password):
    return generate_password_hash(password)


def is_username_unique(username):
    username = username.lower()

    user = user_repository.get_by_username(username)

    result = True

    if user:
        result = False
    return jsonify({"is_unique": result})


def is_email_unique(email):
    user = user_repository.get_by_email(email)
    result = True
    if user:
        result = False
    return result


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
    
# uses email instead of phone
def update_password2(password, email):
    try:
        user = get_by_email(email)
        if user:
            encrypted_password = encrypt_passoword(password)
            result = user_repository.update_password2(encrypted_password, email)
            return result
        raise EmailNotFoundException()
    except Exception as e:
        raise e