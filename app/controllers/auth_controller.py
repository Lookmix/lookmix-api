from flask_jwt_extended import (
    jwt_refresh_token_required, jwt_required,
    get_jwt_identity
)
from app import app, app_blueprint
from flask import request, jsonify
from app.services import auth_service
from app.exceptions.error import BadCredentialsException


@app_blueprint.route('/login', methods=['POST'])
def login():
    try:
        response = auth_service.attempt_login(request.json)

        return response, 201
    except BadCredentialsException:
        return jsonify({"erro":"Dados de login inválidos"}), 401


@app_blueprint.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user_id = get_jwt_identity()

    response = auth_service.refresh_token(current_user_id)

    return response, 201


@app_blueprint.route('/token', methods=['PUT'])
@jwt_required
def logout(): # token_id):
    # current_user_id = get_jwt_identity()

    # auth_service.revoke_old_refresh_token(current_user_id)

    response = auth_service.revoke_token() # token_id)

    return response, 200


@app_blueprint.route("/send_verify_code", methods=['GET'])
def send_verify_code():
    phone = request.args.get("phone")
    return auth_service.send_verify_code(phone)


@app_blueprint.route("/verify_code", methods=['GET'])
def verify_code():
    code = request.args.get("code")
    request_id = request.args.get("request_id")
    return auth_service.verify_code(request_id, code)


app.register_blueprint(app_blueprint, url_prefix="/auth")
