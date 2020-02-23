from app import app
from auth import authentication
from flask import jsonify
from repositories import auth_repository, user_repository


def criar_tokens(request_data):
    user = user_repository.get_by_username(request_data['username'])

    response = authentication.attempt_login(request_data, user)

    save_data_token_in_db(response)

    return jsonify(response)


def refresh_token(current_user):
    response = authentication.refresh_token(current_user)

    save_data_token_in_db(response)

    return jsonify(response)


def revoke_token(token_id):
    token_data = auth_repository.get_by_jti(token_id)
    token_data = authentication.revoke_token(token_data)
    auth_repository.update_revoke(token_id, token_data)
    return jsonify({'is_revoked': True})


def is_token_revoked(token_id):
    token_data = auth_repository.get_by_jti(token_id)

    return authentication.check_is_token_revoked(token_data)


def save_data_token_in_db(response):
    access_token_data = authentication.create_data_token(response['access_token'],
                                   app.config['JWT_IDENTITY_CLAIM'])
    refresh_token_data =authentication.create_data_token(response['refresh_token'],
                                   app.config['JWT_IDENTITY_CLAIM'])
    auth_repository.save_data_tokens([access_token_data, refresh_token_data])