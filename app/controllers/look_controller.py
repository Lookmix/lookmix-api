import json
from flask import Blueprint, request 
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity
)
from jsonschema import ValidationError
from app.services import look_service
from app.exceptions.error import DuplicatedDayOfWeekException
from app.exceptions.error import DuplicatedPeriodException
from app.exceptions.error import PeriodEmptyException
from app.exceptions.error import PeriodTooLongException
from app.exceptions.error import DuplicatedOccasionException
from app.exceptions.error import DuplicatedSortException
from app.exceptions.error import QueueFullException

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
			look_service.dispatch_look_generation(user_id)
			return {}, 204
		raise Exception(result)
	except QueueFullException as error:
		return json.dumps({
			"message": "Servidor sobrecarregado, tente novamente em instantes",
            "error": error.args[0]
		}), 400
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
	except DuplicatedSortException as e:
		return json.dumps({
            "message": "Ordenação do dia da semana duplicada",
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

@bp.route("/list", methods=["GET"])
@jwt_required()
def get_lookset():
	try:
		user_id = get_jwt_identity()
		response = look_service.get_looks(user_id)
		if response == -1:
			look_service.dispatch_look_generation(user_id)
			return json.dumps({
				"user_id": "",
				"looks": [],
				"created_at": "",
				"days_count": 0,
				"total_days": 0
			}), 202
		return json.dumps(response), 200
	except Exception as e:
		print(e)
		return json.dumps({
            "message": "Erro ao tentar recuperar looks",
            "error": "unknow"
        }), 400

@bp.route("/recursive", methods=["GET"])
def get_looksetrecursive():
	try:
		response = look_service.getlooksetrecursive()
		return json.dumps(response), 200
	except Exception as e:
		print(e)
		return json.dumps({
            "message": "Erro ao tentar recuperar lookset recursivo",
            "error": "unknow"
        }), 400

@bp.route("/procedural", methods=["GET"])
def get_looksetprocedural():
	try:
		response = look_service.getlooksetprocedure()
		return json.dumps(response), 200
	except Exception as e:
		print(e)
		return json.dumps({
            "message": "Erro ao tentar recuperar lookset procedural",
            "error": "unknow"
        }), 400
