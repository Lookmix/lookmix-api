from app import app, jwt
from app.auth import authentication
from flask import jsonify
from app.repositories import auth_repository, user_repository


def criar_tokens(request_data):
    user = user_repository.get_by_username(request_data['username'])

    response = authentication.attempt_login(request_data, user)

    save_data_token_in_db(response)

    return jsonify(response)


def refresh_token(user_id):
    revoke_old_refresh_token(user_id)

    response = authentication.refresh_token(user_id)

    save_data_token_in_db(response)

    return jsonify(response)


def revoke_token(token_id):
    token_data = auth_repository.get_by_jti(token_id)
    token_data = authentication.set_revoke_token(token_data)
    auth_repository.update_revoke(token_id, token_data)


def is_token_revoked(token_id):
    token_data = auth_repository.get_by_jti(token_id)

    return authentication.check_is_token_revoked(token_data)


def save_data_token_in_db(response):
    access_token_data = authentication.create_data_token(response['access_token'],
                                   app.config['JWT_IDENTITY_CLAIM'])
    refresh_token_data =authentication.create_data_token(response['refresh_token'],
                                   app.config['JWT_IDENTITY_CLAIM'])
    auth_repository.save_data_tokens([access_token_data, refresh_token_data])


def revoke_old_refresh_token(user_id):
    old_refresh_token = auth_repository.get_non_revoked_refresh_token(user_id)

    if old_refresh_token:
        revoke_token(old_refresh_token['jti'])


# Verifica se o token foi revogado
@jwt.token_in_blacklist_loader
def token_in_blacklist_loader(decoded_token):
    jti = decoded_token['jti']

    return is_token_revoked(jti)