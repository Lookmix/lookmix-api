import datetime
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from bson.objectid import ObjectId
from app.exceptions.error import (
    TokenNaoExisteException,
    DadosLoginInvalidosException
)
from flask import jsonify


# TODO: colocar em um arquivo de constants
expires_access_token = datetime.timedelta(minutes=15)
expires_refresh_token = datetime.timedelta(days=2)


def attempt_login(dados_login, user):

    user_id = str(ObjectId(user["_id"]))

    if user and check_password_hash(user["password"], dados_login["password"]):
        return create_tokens(user_id)
    raise DadosLoginInvalidosException()


def refresh_token(user_id):
    return create_tokens(user_id)


def set_revoke_token(token_data):
    if token_data:
        token_data["revoked"] = True

        response = {"is_disconnected": True}

        unset_jwt_cookies(jsonify(response))

        return {"is_disconnected": response, "token_data": token_data}
    raise TokenNaoExisteException()


def check_is_token_revoked(token_data):
    if token_data:
        response = token_data["revoked"]
        return response
    return True


def create_data_token(encoded_token, identity_claim):
    decoded_token = decode_token(encoded_token)

    data_token = {
        "jti": decoded_token["jti"],
        "token_type": decoded_token["type"],
        "user_id": decoded_token[identity_claim],
        "expires": datetime.datetime.fromtimestamp(decoded_token["exp"]),
        "revoked": False,
    }
    return data_token


def create_tokens(user_id):
    access_token = create_access_token(identity=user_id,
                                       expires_delta=expires_access_token,
                                       fresh=True)
    refresh_token = create_refresh_token(user_id,
                                         expires_delta=expires_refresh_token)
    decoded_access_token = decode_token(access_token)
    decoded_refresh_token = decode_token(refresh_token)
    
    response = jsonify({
        "access_token_data": {
            "expires": datetime.datetime.fromtimestamp(decoded_access_token["exp"]),
            "jti": decoded_access_token["jti"]
        },
        "refresh_token_data": {
            "expires": datetime.datetime.fromtimestamp(decoded_refresh_token["exp"]),
            "jti": decoded_refresh_token["jti"]
        }
    })
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return {
        "response": response,
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def verify_validation_phone_code():
    return 