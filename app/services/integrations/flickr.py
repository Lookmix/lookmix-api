import json
import flickr_api
from app.utils import image_converter

def upload(file, id):
    try:
        set_auth_handler()

        imageJPG = image_converter.convert_to_JPG(file)

        response = flickr_api.upload(
            photo_file=file.filename, 
            title=id,
            photo_file_data=imageJPG, 
            is_public="0",
            is_friend="0",
            is_family="0"
        )
        data = json.loads(json.dumps(response.__dict__))

        return data
    except Exception as e:
        raise e

def get_photo_by_id(id):
	try:
		set_auth_handler()
		authdata = flickr_api.test.login()
		user_id = authdata.id
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

def delete():
    return

def set_auth_handler():
    # TODO: move to .env file
    flickr_api.set_keys(api_key="9259843e2fab63be76733f4a8593aa7f", api_secret="913f8a2084e9a985")
    flickr_api.set_auth_handler("app/.auth.txt")
