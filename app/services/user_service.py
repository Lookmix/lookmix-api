from services import flickr_service
import flickr_api
import json
from repositories import user_repository
from utils import validator_json
from werkzeug.security import generate_password_hash
from bson.json_util import dumps


def save(usuario):
    try:
        if 'is_admin' not in usuario:
            usuario['is_admin'] = False

        validator_json.assert_valid_schema(usuario, "usuario.json")

        password_encrypted = generate_password_hash(usuario['password'])

        usuario['password'] = password_encrypted

        id = user_repository.save(usuario)

        return dumps(id)
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
        # photo.owner.token.access_token = json.dumps(photo.owner.token.access_token.__dict__)
        # photo.owner.token.consumer = json.dumps(photo.owner.token.consumer.__dict__)
        # photo.owner.token = json.dumps(photo.owner.token.__dict__)
        default = lambda o: f"<<non-serializable: {type(o).__qualname__}>>"
        # photo.owner = json.dumps(photo.owner.__dict__, default=default)

        # photo.token.access_token = json.dumps(photo.token.access_token.__dict__)
        # photo.token.consumer = json.dumps(photo.token.consumer.__dict__)
        # photo.token = json.dumps(photo.token.__dict__)
        photo_json = json.dumps(photo.__dict__, default=default)
        photos_list_json.append(json.loads(photo_json))
    return photos_list_json


def get_user_flickr():
    flickr_service.set_auth_handler()
    return flickr_api.test.login()

