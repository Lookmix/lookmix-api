# from 'módulo' import 'variável'
from app import app, app_blueprint
from app.services import flickr_service
from flask import request
import json


@app_blueprint.route("/upload", methods=['POST'])
def upload_file():
    r = request
    files = r.files

    try:
        photos = flickr_service.upload(files)  # ['file']

        return json.dumps(photos), 200
    except Exception as e:
        return json.dumps({
            "message": "Erro ao tentar salvar imagem",
            "error": e.args[0]
        }), 400


@app_blueprint.route("/getAllImages", methods=['GET'])
def get_all_images():
    response = flickr_service.get_all()
    return json.dumps(response.__dict__), 200


app.register_blueprint(app_blueprint, url_prefix="/api")

