import json
from flask import Blueprint, request 
from flask_jwt_extended import jwt_required
from app.services import category_service


bp = Blueprint("category", __name__, url_prefix="/category")

@bp.route("/save", methods=["POST"])
@jwt_required()
def save_category():
	try:
		request_data = request.json

		category_id = category_service.save(request_data)

		return { "id": category_id }, 201
	except Exception as e:
		return json.dumps({
            "message": "Erro ao tentar salvar categoria",
            "error": e.args[0]
        }), 400


@bp.route("/find", methods=["GET"])
@jwt_required()
def get_categories():
    try:
        response = category_service.get_categories()

        return json.dumps(response), 200
    except Exception as e:
        return json.dumps({
            "message": "Erro ao tentar recuperar imagem",
            "error": e.args[0]
        }), 400


@bp.route("/find_by_id", methods=["GET"])
@jwt_required()
def get_category_by_id():
    try:
        id = request.args.get("id")

        response = category_service.get_category_by_id(id)

        return response, 200
    except Exception as e:
        return json.dumps({
            "message": "Erro ao tentar recuperar categoria",
            "error": e.args[0]
        }), 400
