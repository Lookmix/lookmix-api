import json
from flask import Blueprint, request 
from flask_jwt_extended import jwt_required
from app.services import image_service

bp = Blueprint("clothe", __name__, url_prefix="/clothe")

@bp.route("/save", methods=["POST"])
@jwt_required()
def save_clothes():
    JSON_TYPE = "/json"
    IMAGE_TYPE = "image/"
    FORMDATA_IMAGE = "file"
    FORMDATA_DOCUMENT = "document"

    try:
        r = request
        files = r.files
        files_dict = files.to_dict()
        responses = []
        for index, key in enumerate(files_dict):
            content_type = files_dict[key].content_type

            if IMAGE_TYPE in content_type:
                DOCUMENT_KEY = f"{index}{FORMDATA_DOCUMENT}"
                document = files_dict[DOCUMENT_KEY]
                document_json = json.loads(document.read())
                id = document_json.get("id")

                IMAGE_KEY = f"{index}{FORMDATA_IMAGE}"
                image = files_dict[IMAGE_KEY]

                response = image_service.upload(image, id)
                responses.append(response)
        return { "responses": responses }, 201
    except Exception as e:
        return json.dumps({
            "message": "Erro ao tentar salvar imagem",
            "error": e.args[0]
        }), 400

@bp.route("/find_by_id", methods=["GET"])
@jwt_required()
def get_clothe_by_id():
    try:
        id = request.args.get("id")

        response = image_service.get_image(id)

        return response, 200
    except Exception as e:
        return json.dumps({
            "message": "Erro ao tentar recuperar imagem",
            "error": e.args[0]
        }), 400
