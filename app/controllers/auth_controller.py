from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies, 
)
from jwt import InvalidSignatureError, ExpiredSignatureError
from jsonschema import ValidationError
from app.services import auth_service
from app.exceptions.error import (
    BadCredentialsException,
    FailToGenerateOTPException,
    AttemptsExceedException,
    RequiredParamException
)

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
def login():
    try:
        user_id = auth_service.validate_credentials(request.json)

        tokens = auth_service.create_tokens(user_id)

        access = tokens.get("access_token")
        refresh = tokens.get("refresh_token")
        auth_metadata = tokens.get("data")

        response = {}
        response["auth"] = auth_metadata

        auth_service.save_auth_metadata(access)
        auth_service.save_auth_metadata(refresh)

        response = jsonify(response)

        set_access_cookies(response, access)
        set_refresh_cookies(response, refresh)

        return response, 200
    except ValidationError as error:
        return jsonify({
            "message": error.message,
            "error": "validationError"
        }), 400
    except BadCredentialsException:
        return jsonify({
            "message": "Bad credentials",
            "error":"badCredencials"
        }), 401


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()

    response = auth_service.refresh_token(current_user_id)

    return response, 201


@bp.route('/token', methods=['PUT'])
@jwt_required()
def logout(): # token_id):
    # current_user_id = get_jwt_identity()

    # auth_service.revoke_old_refresh_token(current_user_id)

    response = auth_service.revoke_token() # token_id)

    return response, 200


@bp.route("/get_otp", methods=['GET'])
def get_otp():
    try:
        phone = request.args.get("phone")

        if phone is not None:
            return auth_service.handle_otp(phone)
        raise RequiredParamException("parameter 'phone' is required")
    except FailToGenerateOTPException as e:
        return jsonify({
            "message": str(e),
            "error": "failToGenerateOTP"
        }), 400
    except RequiredParamException as e:
        return jsonify({
            "error": "requiredParam", 
            "message": str(e)
        }), 400


@bp.route("/verify_otp", methods=['POST'])
def verify_otp():
    try:
        request_data = request.json

        param_reset_pass = request.args.get("reset_password")

        response = auth_service.verify_otp(request_data)

        otp_id = request_data.get("id")

        tokens = auth_service.create_tokens(otp_id)

        access = tokens.get("access_token")
        refresh = tokens.get("refresh_token")
        auth_metadata = tokens.get("data")

        response["auth"] = auth_metadata

        reset_password = False

        if param_reset_pass is not None:
            reset_password = True

        auth_service.save_auth_metadata(access, reset_password, not reset_password)
        auth_service.save_auth_metadata(refresh, reset_password, not reset_password)

        response = jsonify(response)

        set_access_cookies(response, access)
        set_refresh_cookies(response, refresh)

        return response, 200
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


@bp.route("/verify_access", methods=['GET'])
@jwt_required()
def verify_access():
    return { "valid": True }, 200
