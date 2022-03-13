from PIL import Image
from io import BytesIO


def convert_to_JPG(image):
    file = BytesIO()
    im = Image.open(image)
    im.save(file, "JPEG")
    file.name = image.filename
    file.seek(0)
    return file


