# from 'módulo' import 'variável'
from app import app, app_blueprint
from flask import request
from flask import jsonify
import json
from services import user_service
from jsonschema import ValidationError
from flask_jwt_extended import jwt_required

# from flask_jwt import jwt_required, current_identity


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

        id = user_service.save(request_data)

        return id, 200
    except ValidationError as validationError:
        return json.dumps({'erro': validationError.message}), 400
    except Exception as e:
        retorno = str(e)
        return json.dumps(retorno), 400


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


@app_blueprint.route("/get_photos", methods=['GET'])
def get_photos():
    photos = user_service.get_photos()

    return json.dumps(photos), 200


app.register_blueprint(app_blueprint, url_prefix="/api/usuarios")