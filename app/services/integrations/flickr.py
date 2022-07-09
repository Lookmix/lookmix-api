import json
import uuid
import flickr_api
from app import app
from app.utils import image_converter


def upload(file, closet_id):
    print("uploading image...")
    try:
        set_auth_handler()

        imageJPG = image_converter.convert_to_JPG(file)

        response = flickr_api.upload(
            photo_file=file.filename,
            photo_file_data=imageJPG, 
            is_public="0",
            is_friend="0",
            is_family="0"
        )
        data = json.loads(json.dumps(response.__dict__))
        photo_id = data.get("id")
        save_photo_in_closet(photo_id, closet_id)

        photo_details = get_photo_details_by_id(photo_id)
        server_id = photo_details.get("server")
        secret = photo_details.get("secret")
        size ="n"
        photo_url = f"https://live.staticflickr.com/{server_id}/{photo_id}_{secret}_{size}.jpg"
        return photo_url
    except Exception as e:
        raise e


def create_closet():
    print("creating closet...")
    try:
        set_auth_handler()
        response = flickr_api.Photoset.create(
            title=str(uuid.uuid4()),
            primary_photo_id="52100247230"
        )
        del response.__dict__["token"]
        del response.__dict__["primary"]
        data = json.loads(json.dumps(response.__dict__))
        print(data)
        id = data.get("id")
        return id
    except Exception as e:
        raise e


def save_photo_in_closet(photo_id, closet_id):
    print("saving image into closet...")
    try:
        set_auth_handler()
        photoset = flickr_api.Photoset(id=closet_id)
        photoset.addPhoto(
            photo_id=photo_id,
            photoset_id=closet_id
        )
    except Exception as e:
        raise e


def get_photo_details_by_id(id):
    try:
        set_auth_handler()
        photo = flickr_api.Photo(id=id)
        response = photo.getInfo()
        return response
    except Exception as e:
        raise e


def get_photo_by_id(id):
    try:
        set_auth_handler()
        user_id = get_user_id()
        response = flickr_api.Photo.search(
            user_id=user_id,
            text=id,
            per_page=10
		)
        del response[0].__dict__["owner"]
        del response[0].__dict__["token"]
        return response[0].__dict__
    except Exception as e:
        raise e


def get_all():
    return []


def delete(photo_ids):
    try:
        set_auth_handler()
        for id in photo_ids:
            photo = flickr_api.Photo(id=id)
            photo.delete()
    except Exception as e:
        raise e


def delete_from_closet(closet_id, photo_ids):
    try:
        if isinstance(photo_ids, list):
            photo_ids = u",".join(photo_ids)

        set_auth_handler()
        photoset = flickr_api.Photoset(id=closet_id)
        photoset.removePhotos(photo_ids=photo_ids)
    except Exception as e:
        raise e


def get_user_id():
    authdata = flickr_api.test.login()
    user_id = authdata.id
    return user_id


def set_auth_handler():
    api_key = app.config.get("FLICKR_API_KEY")
    api_secret = app.config.get("FLICKR_API_SECRET")
    access_token_key = app.config.get("FLICKR_ACCESS_KEY")
    access_token_secret = app.config.get("FLICKR_ACCESS_SECRET")

    flickr_api.set_keys(
        api_key=api_key, 
        api_secret=api_secret
    )
    auth_handler = flickr_api.auth.AuthHandler(
        access_token_key=access_token_key,
        access_token_secret=access_token_secret
    )
    flickr_api.set_auth_handler(auth_handler)


"""
HOW TO GET TOKEN

In the terminal, activate venv:

>>> cd backend
>>> . venv/bin/activate

In the same terminal execute python shell:

>>> python3

Into the python shell, setup and get token:

>>> import flickr_api
>>> api_key = "replace_by_api_key"
>>> api_secret = "replace_by_api_secret"
>>> flickr_api.set_keys(api_key=api_key, api_secret=api_secret)
>>> auth_handler = flickr_api.auth.AuthHandler()
>>> url = auth_handler.get_authorization_url(perms="delete")
>>> print(url)

Copy the printed url, paste on browser and authorize

- Url example: https://www.flickr.com/services/oauth/authorize?oauth_token=72157720849868113-8adbb68f9614d576&perms=delete

Copy the value of oauth_verifier xml tag

- oauth_verifier example: "e524c8b5b87cf59a"

Back to running python shell and finish the setup:

>>> auth_handler.set_verifier("replace_by_oauth_verifier")
>>> flickr_api.set_auth_handler(auth_handler)
>>> auth_handler.save(".auth.txt")

On this step, the python shell can be closed

Open auth.txt file

Copy and paste the first line on FLICKR_ACCESS_KEY env var

Copy and paste the second line on FLICKR_ACCESS_SECRET env var
"""