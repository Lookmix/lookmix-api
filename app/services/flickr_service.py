import flickr_api
import uuid
import json
from utils import image_converter


def upload(files):
    try:
        set_auth_handler()

        response_data = []

        for f in files:
            imageJPG = image_converter.converter_para_JPG(files[f])

            response = flickr_api.upload(photo_file=files[f].filename, title=str(uuid.uuid4()),
                              photo_file_data=imageJPG, is_public='0',
                              is_friend='0', is_family='0')
            response_data.append(json.loads(json.dumps(response.__dict__)))
        return response_data
    except Exception as e:
        raise e


def get_all():
    return None


def delete():
    return


def set_auth_handler():
    flickr_api.set_keys(api_key="9259843e2fab63be76733f4a8593aa7f", api_secret="913f8a2084e9a985")
    flickr_api.set_auth_handler("app/.auth.txt")
