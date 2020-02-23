from flask_jwt_extended import (
    jwt_refresh_token_required, jwt_required,
    get_jwt_identity
)
from app import app, app_blueprint, jwt
from flask import request, jsonify
from services import auth_service
from exceptions.error import TokenNaoExisteException, DadosLoginInvalidosException


@app_blueprint.route('/auth/login', methods=['POST'])
def login():
    try:
        response = auth_service.criar_tokens(request.json)

        return response, 201
    except DadosLoginInvalidosException:
        return jsonify({"erro":"Dados de login inválidos"}), 401


@app_blueprint.route('/auth/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()

    tokens = auth_service.refresh_token(current_user)

    return tokens, 201


@app_blueprint.route('/auth/token/<token_id>', methods=['PUT'])
@jwt_required
def logout(token_id):
    try:
        return auth_service.revoke_token(token_id), 200
    except TokenNaoExisteException:
        return jsonify({'erro': 'The specified token was not found'}), 404


@jwt.token_in_blacklist_loader
def is_token_revoked(decoded_token):
    jti = decoded_token['jti']

    return auth_service.is_token_revoked(jti)
# jti = get_raw_jwt()['jti']


app.register_blueprint(app_blueprint, url_prefix="/api")
