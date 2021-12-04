from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from app import app, app_blueprint
from flask import request, jsonify
from app.services import auth_service
from app.exceptions.error import (
    BadCredentialsException,
    FailToGenerateVerifyCodeException,
    AttemptsExceedException,
    RequiredParamException
)
from jsonschema import ValidationError
from jwt import InvalidSignatureError, ExpiredSignatureError

@app_blueprint.route('/login', methods=['POST'])
def login():
    try:
        response = auth_service.attempt_login(request.json)

        return response, 200
    except BadCredentialsException:
        return jsonify({"erro":"Dados de login inválidos"}), 401


@app_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()

    response = auth_service.refresh_token(current_user_id)

    return response, 201


@app_blueprint.route('/token', methods=['PUT'])
@jwt_required()
def logout(): # token_id):
    # current_user_id = get_jwt_identity()

    # auth_service.revoke_old_refresh_token(current_user_id)

    response = auth_service.revoke_token() # token_id)

    return response, 200


@app_blueprint.route("/send_verify_code", methods=['GET'])
def send_verify_code():
    try:
        phone = request.args.get("phone")
        
        if phone is not None:
            return auth_service.handle_OTP(phone)
        raise RequiredParamException("'phone' param is required")
    except FailToGenerateVerifyCodeException as e:
        return jsonify({"error": str(e)}), 400
    except RequiredParamException as e:
        return jsonify({"error": str(e)}), 400


@app_blueprint.route("/verify_code", methods=['POST'])
def verify_code():
    try:
        request_data = request.json

        return auth_service.verify_code(request_data)
    except ValidationError as error:
        return jsonify({
            "error": "validationError",
            "message": error.message
        }), 400
    except AttemptsExceedException:
        return jsonify({
            "error": "attempsExceed",
            "message": "Attemps Exceed"
        }), 400
    except InvalidSignatureError:
        return jsonify({
            "error": "invalidOTP",
            "message": "Invalid OTP"
        }), 400
    except ExpiredSignatureError:
        return jsonify({
            "error": "expired",
            "message": "Token has been expirated"
        }), 400

app.register_blueprint(app_blueprint, url_prefix="/auth")
