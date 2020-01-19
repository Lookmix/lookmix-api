# from 'módulo' import 'variável'
from app import app, app_blueprint
from ..flickr_service import *
from flask import request
import json
from io import BytesIO
from PIL import Image


@app_blueprint.route("/upload", methods=['POST'])
def upload_file():
    file = request.files['file']

    response = upload(file)

    return json.dumps(response.__dict__), 200


@app_blueprint.route("/getAllImages", methods=['GET'])
def get_all_images():
    response = get_all()
    return json.dumps(response.__dict__), 200


app.register_blueprint(app_blueprint, url_prefix="/api")

