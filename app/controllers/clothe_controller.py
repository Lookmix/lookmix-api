import json
from flask import Blueprint, request 
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity
)
from app.services import image_service
from app.services import user_service
from app.services import closet_service
from app.services import clothe_service

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

        user_id = get_jwt_identity()
        closet = closet_service.get_closet_by_user_id(user_id)
        closet_id = 0
        if closet:
            closet_id = closet.get("_id")
        if not closet_id:
            closet_id = image_service.create_closet()
            closet_service.create(closet_id, user_id)

        count = 0
        for index, key in enumerate(files_dict):
            content_type = files_dict[key].content_type
            if IMAGE_TYPE in content_type:
                IMAGE_KEY = f"{count}{FORMDATA_IMAGE}"
                image = files_dict[IMAGE_KEY]
                image_response = image_service.upload(image, closet_id)
                DOCUMENT_KEY = f"{count}{FORMDATA_DOCUMENT}"
                document = files_dict[DOCUMENT_KEY]
                document_json = json.loads(document.read())
                document_json["image"] = image_response
                clothe_service.create(document_json, closet_id)
                responses.append(image_response)
                count+=1
        return { "images": responses }, 201
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


@bp.route("/find_by_closet_id", methods=["GET"])
@jwt_required()
def get_clothes_by_closet_id():
    try:
        user_id = get_jwt_identity()
        closet = closet_service.get_closet_by_user_id(user_id)
        closet_id = 0

        if closet:
            closet_id = closet.get("_id")
        if not closet_id:
            closet_id = image_service.create_closet()
            closet_service.create(closet_id, user_id)

        response = clothe_service.get_clothes_by_closet_id(closet_id)

        return {"clothes": response}, 200
    except Exception as e:
        return json.dumps({
            "message": "Erro ao tentar recuperar peças",
            "error": e.args[0]
        }), 400
