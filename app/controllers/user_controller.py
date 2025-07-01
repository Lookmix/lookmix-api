import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from jsonschema import ValidationError
from app.services import user_service, auth_service
from app.exceptions.error import (
    DuplicatedPhoneException, 
    PhoneNotFoundException,
    EmailNotFoundException,
    DuplicatedEmailException
)

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/protected', methods=['POST'])
@jwt_required()
def protected():
    # response = '%s' % current_identity
    # return response, 200
    return jsonify([True]), 200


@bp.route("/save", methods=['POST'])
@jwt_required()
def add_user():
    try:
        request_data = request.json
        user_id = user_service.save(request_data)
        return jsonify({
            "id": user_id
        }), 200
    except ValidationError as error:
        validator = error.validator
        customErrorMessage = error.schema.get("errorMessage", {}).get(validator)
        message = error.message
        if customErrorMessage is not None:
            message = customErrorMessage
        return jsonify({
            "error": "validationError",
            "message": message
        }), 400
    except DuplicatedPhoneException:
        return jsonify({
            "error": "duplicatedPhone",
            "message": "Duplicated phone"
        }), 400
    except Exception as e:
        return jsonify({
            "error": "unknow",
            "message": str(e)
        }), 400


# uses email instead of phone
@bp.route("/save2", methods=['POST'])
@jwt_required()
def add_user2():
    try:
        request_data = request.json
        user_id = user_service.save2(request_data)
        return jsonify({
            "id": user_id
        }), 200
    except ValidationError as error:
        validator = error.validator
        customErrorMessage = error.schema.get("errorMessage", {}).get(validator)
        message = error.message
        if customErrorMessage is not None:
            message = customErrorMessage
        return jsonify({
            "error": "validationError",
            "message": message
        }), 400
    except DuplicatedEmailException:
        return jsonify({
            "error": "duplicatedEmail",
            "message": "Duplicated email"
        }), 400
    except Exception as e:
        return jsonify({
            "error": "unknow",
            "message": str(e)
        }), 400


@bp.route("/get_all", methods=['GET'])
@jwt_required()
def get_all():
    try:
        users = user_service.get_all()

        return users, 200
    except Exception as e:
        return jsonify({'error': e}), 400


@bp.route("/get_user", methods=['GET'])
@jwt_required()
def get_user_flickr():
    user = user_service.get_user_flickr()

    return json.dumps(user.__dict__), 200


@bp.route("/update_password", methods=['PUT'])
@jwt_required()
def update_password():
    try:
        request_data = request.json

        phone = request_data['phone']
        new_password = request_data['password']

        result = user_service.update_password(new_password, phone)
        if result > 0:
            response = auth_service.revoke_token()

            return response, 200
        raise PhoneNotFoundException
    except PhoneNotFoundException:
        return jsonify({
            "error": "phoneNotFound",
            "message": "Phone does exist"
        }), 400
    except Exception as e:
        return jsonify({
            "error": "unknow",
            "message": str(e)
        }), 400


# uses email instead of phone
@bp.route("/update_password2", methods=['PUT'])
@jwt_required()
def update_password2():
    try:
        request_data = request.json
        email = request_data['email']
        new_password = request_data['password']
        result = user_service.update_password(new_password, email)
        if result > 0:
            response = auth_service.revoke_token()
            return response, 200
        raise EmailNotFoundException
    except EmailNotFoundException:
        return jsonify({
            "error": "emailNotFound",
            "message": "Email does exist"
        }), 400
    except Exception as e:
        return jsonify({
            "error": "unknow",
            "message": str(e)
        }), 400


@bp.route("/get_photos", methods=['GET'])
@jwt_required()
def get_photos():
    photos = user_service.get_photos()

    return json.dumps(photos), 200


@bp.route("/is_email_unique", methods=['GET'])
def is_email_unique():
    phone = request.args.get("email")
    result = user_service.is_email_unique(phone)
    return {"is_unique": result}, 200


@bp.route("/is_phone_unique", methods=['GET'])
def is_phone_unique():
    phone = request.args.get("phone")

    result = user_service.is_phone_unique(phone)

    return {"is_unique": result}, 200


@bp.route("/is_username_unique/<phone>", methods=['GET'])
def is_username_unique(phone):
    return user_service.is_username_unique(phone), 200


