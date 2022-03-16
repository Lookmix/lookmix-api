import json
from flask import Blueprint, request 
from app.services import flickr_service

bp = Blueprint('file', __name__, url_prefix='/file')

@bp.route("/upload", methods=['POST'])
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


@bp.route("/getAllImages", methods=['GET'])
def get_all_images():
    response = flickr_service.get_all()
    return json.dumps(response.__dict__), 200

