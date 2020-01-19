import flickr_api
import uuid


def upload(file):
    flickr_api.set_keys(api_key="9259843e2fab63be76733f4a8593aa7f", api_secret="913f8a2084e9a985")
    flickr_api.set_auth_handler("app/.auth.txt")
    return flickr_api.upload(photo_file=file, title=str(uuid.uuid4()), photo_file_data=file)


def get_all():
    return None


def delete():
    return


