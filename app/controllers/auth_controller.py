import urllib.parse

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
    RequiredParamException,
    FailToSendEmailException
)

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
def login():
    try:
        user_id = auth_service.validate_credentials(request.json)

        response = auth_service.handle_tokens(user_id)

        return response, 200
    except ValidationError as error:
        return jsonify({
            "message": error.message,
            "error": "validationError"
        }), 400
    except BadCredentialsException:
        return jsonify({
            "message": "Bad credentials",
            "error":"badCredentials"
        }), 401


# uses email instead of phone
@bp.route('/login2', methods=['POST'])
def login2():
    try:
        user_id = auth_service.validate_credentials2(request.json)
        response = auth_service.handle_tokens(user_id)
        return response, 200
    except ValidationError as error:
        return jsonify({
            "message": error.message,
            "error": "validationError"
        }), 400
    except BadCredentialsException:
        return jsonify({
            "message": "Bad credentials",
            "error":"badCredentials"
        }), 401


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()

    response = auth_service.handle_tokens(user_id)

    return response, 200


@bp.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
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


# uses email instead of phone
@bp.route("/get_otp2", methods=['GET'])
def get_otp2():
    try:
        email = request.args.get("email")
        is_pass_reset = request.args.get("is_pass_reset", False, type=bool)
        if email is not None:
            email = urllib.parse.unquote(email)
            return auth_service.handle_otp2(email, is_pass_reset=is_pass_reset)
        raise RequiredParamException("parameter 'email' is required")
    except FailToSendEmailException as e:
        return jsonify({
            "error": "failToSendEmail",
            "message": str(e) # TODO: rename key to description
        }), 400
    except FailToGenerateOTPException as e:
        return jsonify({
            "message": str(e),
            "error": "failToGenerateOTP"
        }), 400
    except RequiredParamException as e:
        return jsonify({
            "error": "requiredParam", 
            "message": str(e) # TODO: rename key to description
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
