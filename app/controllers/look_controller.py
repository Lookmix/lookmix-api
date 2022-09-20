import json
from flask import Blueprint, request 
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity
)
from app.services import look_service
from app.exceptions.error import DuplicatedDayOfWeekException
from app.exceptions.error import DuplicatedPeriodException
from app.exceptions.error import PeriodEmptyException
from app.exceptions.error import PeriodTooLongException

bp = Blueprint("look", __name__, url_prefix="/look")

@bp.route("/save_daily_look_setup", methods=["POST"])
@jwt_required()
def save_daily_look_setup():
	try:
		request_data = request.json
		user_id = get_jwt_identity()
		data = { 
			"days_of_week": request_data,
			"user_id": user_id
		} 
		result = look_service.save_daily_look_setup(user_id, data)
		if result > 0:
			return {}, 204
	except DuplicatedDayOfWeekException as e:
		return json.dumps({
            "message": "Dia da semana duplicado, devem ser únicos",
            "error": e.args[0]
        }), 400
	except DuplicatedPeriodException as e:
		return json.dumps({
            "message": "Período duplicado, devem ser únicos dentro de cada array da ocasião",
            "error": e.args[0]
        }), 400
	except PeriodEmptyException as e:
		return json.dumps({
            "message": "Nenhum período foi enviado, deve haver pelo menos um para cada ocasião",
            "error": e.args[0]
        }), 400
	except PeriodTooLongException as e:
		return json.dumps({
            "message": "Não podem haver mais de dois períodos por ocasião",
            "error": e.args[0]
        }), 400
	except Exception as e:
		return json.dumps({
            "message": "Erro ao tentar salvar rotina semanal",
            "error": e.args[0]
        }), 400

@bp.route("/find_daily_look_setup_by_user_id", methods=["GET"])
@jwt_required()
def get_daily_look_setup_by_user_id():
	try:
		user_id = get_jwt_identity()
		response = look_service.get_daily_look_setup_by_user_id(user_id)
		if response is not None:
			return response, 200
		return json.dumps(response), 200
	except Exception as e:
		return json.dumps({
            "message": "Erro ao tentar recuperar rotina de looks",
            "error": e.args[0]
        }), 400