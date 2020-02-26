from flask_jwt_extended import (
    jwt_refresh_token_required, jwt_required,
    get_jwt_identity
)
from app import app, app_blueprint, jwt
from flask import request, jsonify
from app.services import auth_service
from app.exceptions.error import TokenNaoExisteException, DadosLoginInvalidosException


@app_blueprint.route('/auth/login', methods=['POST'])
def login():
    try:
        response = auth_service.attempt_login(request.json)

        return response, 201
    except DadosLoginInvalidosException:
        return jsonify({"erro":"Dados de login inválidos"}), 401


@app_blueprint.route('/auth/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user_id = get_jwt_identity()

    response = auth_service.refresh_token(current_user_id)

    return response, 201


@app_blueprint.route('/auth/token/<token_id>', methods=['PUT'])
@jwt_required
def logout(token_id):
    try:
        current_user_id = get_jwt_identity()

        auth_service.revoke_old_refresh_token(current_user_id)

        response = auth_service.revoke_token(token_id)

        return response, 200
    except TokenNaoExisteException:
        return jsonify({'erro': 'The specified token was not found'}), 404


app.register_blueprint(app_blueprint, url_prefix="/api")
