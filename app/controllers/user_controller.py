# from 'módulo' import 'variável'
import json
from app import app, app_blueprint
from flask import request
from flask import jsonify
from app.services import user_service
from jsonschema import ValidationError
from flask_jwt_extended import jwt_required
from app.exceptions.error import DuplicatedPhoneException, DuplicatedUsernameException, PhoneNotFoundException


@app_blueprint.route('/protected', methods=['POST'])
@jwt_required
def protected():
    # response = '%s' % current_identity
    # return response, 200
    return jsonify([True]), 200


@app_blueprint.route("/save", methods=['POST'])
@jwt_required
def add_user():
    try:
        request_data = request.json

        user_id = user_service.save(request_data)

        return jsonify({"id": user_id}), 200
    except ValidationError as error:
        validator = error.validator
        customErrorMessage = error.schema.get("errorMessage", {}).get(validator)
        message = error.message

        if customErrorMessage is not None:
            message = customErrorMessage
        return jsonify({'error': message}), 400
    except DuplicatedPhoneException:
        return jsonify({'error': 'Telefone duplicado'}), 400
    except Exception as e:
        response = str(e)
        return jsonify(response), 400


@app_blueprint.route("/get_all", methods=['GET'])
@jwt_required
def get_all():
    try:
        users = user_service.get_all()

        return users, 200
    except Exception as e:
        return jsonify({'error': e}), 400


@app_blueprint.route("/get_user", methods=['GET'])
@jwt_required
def get_user_flickr():
    user = user_service.get_user_flickr()

    return json.dumps(user.__dict__), 200


@app_blueprint.route("/update_password/<phone>", methods=['PUT'])
@jwt_required
def update_password(phone):
    try:
        request_data = request.json

        response = user_service.update_password(request_data['password'], phone)

        return jsonify({"success": response}), 200
    except PhoneNotFoundException:
        return jsonify({'error': 'Telefone não existe'}), 400
    except Exception as e:
        response = str(e)
        return jsonify(response), 400


@app_blueprint.route("/get_photos", methods=['GET'])
@jwt_required
def get_photos():
    photos = user_service.get_photos()

    return json.dumps(photos), 200


@app_blueprint.route("/is_phone_unique", methods=['GET'])
def is_phone_unique():
    phone = request.args.get("phone")
    return user_service.is_phone_unique(phone), 200


@app_blueprint.route("/is_username_unique/<phone>", methods=['GET'])
def is_username_unique(phone):
    return user_service.is_username_unique(phone), 200


app.register_blueprint(app_blueprint, url_prefix="/users")

