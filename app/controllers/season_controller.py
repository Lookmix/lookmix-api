import json
from flask import Blueprint 
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity
)
from app.services import season_service
from app.services import user_service
# from app import app

bp = Blueprint("season", __name__, url_prefix="/season")


@bp.route("/find", methods=["GET"])
@jwt_required()
def get_seasons():
    try:
        response = season_service.get_seasons()
        return json.dumps(response), 200
    except Exception as e:
        return json.dumps({
            "message": "Erro ao tentar recuperar estações",
            "error": e.args[0]
        }), 400


@bp.route("/current_weather", methods=["GET"])
@jwt_required()
def get_daily_min_and_max_temperatures():
    try:
        # request_data = request.json
        user_id = get_jwt_identity()
        user = user_service.get_by_id(user_id)
        lat = user.get("lat")
        long = user.get("long")
        response = season_service.get_daily_min_and_max_temperatures(lat, long)
        return json.dumps(response), 200
    except Exception as e:
        return json.dumps({
            "message": "Erro ao recuperar clima de hoje",
            "error": e.args[0]
        }), 400