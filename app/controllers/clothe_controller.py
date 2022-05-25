import json
from flask import Blueprint, request 
from flask_jwt_extended import jwt_required

bp = Blueprint("clothe", __name__, url_prefix="/clothe")

@bp.route("/save", methods=["POST"])
@jwt_required()
def save_clothes():
    try:
        r = request
        files = r.files
        for f in files:
          print(f.type, f.name)
        # photos = flickr_service.upload(files)  # ['file']

        # return json.dumps(photos), 200
        return { "success": True }, 200
    except Exception as e:
        return json.dumps({
            "message": "Erro ao tentar salvar imagem",
            "error": e.args[0]
        }), 400

