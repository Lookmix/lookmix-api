from app.services.integrations import flickr
from app.services import user_service


def upload(file, closet_id):
    try:
        return flickr.upload(file, closet_id)
    except Exception as e:
        raise e


def create_closet():
    try:
        closet_id = flickr.create_closet()
        return closet_id
    except Exception as e:
        raise e


def get_image(id):
    try:
        return flickr.get_photo_by_id(id)
    except Exception as e:
        raise e


def delete_images(closet_id, photo_ids):
    print("Deleting image_service")
    try:
        flickr.delete(closet_id, photo_ids)
    except Exception as e:
        raise e