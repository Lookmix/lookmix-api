import flickr_api
import uuid


def upload(files):
    try:
        flickr_api.set_keys(api_key="9259843e2fab63be76733f4a8593aa7f", api_secret="913f8a2084e9a985")
        flickr_api.set_auth_handler("app/.auth.txt")

        for f in files:
            flickr_api.upload(photo_file=files[f].filename, title=str(uuid.uuid4()), photo_file_data=files[f])
    except Exception as e:
        raise e


def get_all():
    return None


def delete():
    return


