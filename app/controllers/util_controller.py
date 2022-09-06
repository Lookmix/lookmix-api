import json
from flask import Blueprint, request 
from flask_jwt_extended import jwt_required
from app.services import util_service


bp = Blueprint("util", __name__)

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