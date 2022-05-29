from app.services.integrations import flickr
from app.services import user_service


def upload(file, closet_id):
    try:
        return flickr.upload(file, closet_id)
    except Exception as e:
        raise e


def create_closet():
    try:
        closet = flickr.create_closet()
        return closet
    except Exception as e:
        raise e


def get_image(id):
    try:
        return flickr.get_photo_by_id(id)
    except Exception as e:
        raise e