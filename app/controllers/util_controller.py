import json
from flask import Blueprint, request 
from flask_jwt_extended import jwt_required
from app.services import util_service


bp = Blueprint("util", __name__)

@bp.route("/occasion/save", methods=["POST"])
@jwt_required()
def save_occasion():
	try:
		request_data = request.json

		util_service.save_occasion(request_data)

		return { "success": True }, 201
	except Exception as e:
		return json.dumps({
			"message": "Erro ao tentar salvar ocasião",
			"error": e.args[0]
	    }), 400


@bp.route("/occasion/find", methods=["GET"])
@jwt_required()
def get_occasions():
    try:
        response = util_service.get_occasions()

        return json.dumps(response.get("occasions")), 200
    except Exception as e:
        return json.dumps({
            "message": "Erro ao tentar recuperar ocasiões",
            "error": e.args[0]
        }), 400


@bp.route("/season/find", methods=["GET"])
@jwt_required()
def get_seasons():
    try:
        response = util_service.get_seasons()

        return json.dumps(response.get("seasons")), 200
    except Exception as e:
        return json.dumps({
            "message": "Erro ao tentar recuperar estações",
            "error": e.args[0]
        }), 400