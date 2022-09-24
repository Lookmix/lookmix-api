import json
from flask import Blueprint, request 
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity
)
from app.services import look_service
from jsonschema import ValidationError
from app.exceptions.error import DuplicatedDayOfWeekException
from app.exceptions.error import DuplicatedPeriodException
from app.exceptions.error import PeriodEmptyException
from app.exceptions.error import PeriodTooLongException
from app.exceptions.error import DuplicatedOccasionException

bp = Blueprint("look", __name__, url_prefix="/look")

@bp.route("/update_daily_look_setup", methods=["PUT"])
@jwt_required()
def update_daily_look_setup():
	try:
		request_data = request.json
		user_id = get_jwt_identity()
		data = { 
			"days_of_week": request_data,
			"user_id": user_id
		} 
		result = look_service.update_daily_look_setup(user_id, data)
		if result == 0 or result is None or result > 0:
			return {}, 204
		raise Exception(result)
	except ValidationError as error:
		validator = error.validator
		customErrorMessage = error.schema.get("errorMessage", {}).get(validator)
		message = error.message
		if customErrorMessage is not None:
			message = customErrorMessage
		return json.dumps({
            "error": "validationError",
            "message": message
        }), 400
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
	except DuplicatedOccasionException as e:
		return json.dumps({
            "message": "Ocasião duplicada, devem ser únicas dentro de cada array da ocasião",
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
            "error": "unknow"
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