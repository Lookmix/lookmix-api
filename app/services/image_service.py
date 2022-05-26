from app.services.integrations import flickr

def upload(file, id):
    try:
        return flickr.upload(file, id)
    except Exception as e:
        raise e

def get_image(id):
    try:
        return flickr.get_photo_by_id(id)
    except Exception as e:
        raise e