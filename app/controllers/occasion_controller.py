import json
from flask import Blueprint, request 
from flask_jwt_extended import jwt_required
from app.services import occasion_service


bp = Blueprint("occasion", __name__, url_prefix="/occasion")

@bp.route("/save", methods=["POST"])
@jwt_required()
def save_occasion():
	try:
		request_data = request.json
		occasion_service.save_occasion(request_data)
		return { "success": True }, 201
	except Exception as e:
		return json.dumps({
			"message": "Erro ao tentar salvar ocasião",
			"error": e.args[0]
	    }), 400

@bp.route("/update", methods=["PUT"])
@jwt_required()
def update_occasion():
    try:
        id_list = request.json
        result = occasion_service.update_by_id(id_list)
        return { "updated": result }, 200
    except Exception as e:
        return json.dumps({
            "message": "Erro ao tentar atualizar ocasião",
            "error": e.args[0]
        }), 400

@bp.route("/find", methods=["GET"])
@jwt_required()
def get_occasions():
	try:
		id = request.args.get("id")
		response = None
		if id is not None:
			response = occasion_service.get_by_id(id)
		else:
			response = occasion_service.get_occasions()
		return json.dumps(response), 200
	except Exception as e:
		return json.dumps({
            "message": "Erro ao tentar recuperar ocasiões",
            "error": e.args[0]
        }), 400

@bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_occasion():
    try:
        response = occasion_service.get_occasions()
        return json.dumps(response.get("occasions")), 200
    except Exception as e:
        return json.dumps({
            "message": "Erro ao tentar deletar ocasião",
            "error": e.args[0]
        }), 400
