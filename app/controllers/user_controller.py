# from 'módulo' import 'variável'
import json
from app import app, app_blueprint
from flask import request
from flask import jsonify
from app.services import user_service
from jsonschema import ValidationError
from flask_jwt_extended import jwt_required
from app.exceptions.error import TelefoneDuplicadoException, UsernameDuplicadoException, TelefoneNaoExisteException


@app_blueprint.route('/protected', methods=['POST'])
@jwt_required
def protected():
    # response = '%s' % current_identity
    # return response, 200
    return jsonify([True]), 200


@app_blueprint.route("/save", methods=['POST'])
def cadastrar_usuario():
    try:
        request_data = request.json

        user_id = user_service.save(request_data)

        return jsonify({"id": user_id}), 200
    except ValidationError as validationError:
        return json.dumps({'erro': validationError.message}), 400
    except TelefoneDuplicadoException:
        return json.dumps({'erro': 'Telefone duplicado'}), 400
    except UsernameDuplicadoException:
        return json.dumps({'erro': 'Username duplicado'}), 400
    except Exception as e:
        resposta = str(e)
        return json.dumps(resposta), 400


@app_blueprint.route("/get_all", methods=['GET'])
def get_all():
    try:
        usuarios = user_service.get_all()

        return usuarios, 200
    except Exception as e:
        return jsonify({'Erro': e}), 400


@app_blueprint.route("/get_user", methods=['GET'])
def get_user_flickr():
    user = user_service.get_user_flickr()

    return json.dumps(user.__dict__), 200


@app_blueprint.route("/update_password/<phone>", methods=['PUT'])
def update_password(phone):
    try:
        request_data = request.json

        response = user_service.update_password(request_data['password'], phone)

        return jsonify({"Sucesso": response}), 200
    except TelefoneNaoExisteException:
        return jsonify({'erro': 'Telefone não existe'}), 400
    except Exception as e:
        resposta = str(e)
        return json.dumps(resposta), 400


@app_blueprint.route("/get_photos", methods=['GET'])
def get_photos():
    photos = user_service.get_photos()

    return json.dumps(photos), 200


@app_blueprint.route("/is_phone_unique/<phone>", methods=['GET'])
def is_phone_unique(phone):
    return user_service.is_phone_unique(phone), 200


@app_blueprint.route("/is_username_unique/<phone>", methods=['GET'])
def is_username_unique(phone):
    return user_service.is_username_unique(phone), 200


app.register_blueprint(app_blueprint, url_prefix="/api/usuarios")

