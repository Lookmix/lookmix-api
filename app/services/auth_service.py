from app import app, jwt
from app.auth import authentication
from flask import jsonify
from app.repositories import auth_repository, user_repository
import requests
import jwt
import random
import datetime

JWT_ALG = "HS256"

def attempt_login(request_data):
    user = user_repository.get_by_phone(request_data["phone"])

    response = authentication.attempt_login(request_data, user)

    save_data_token_in_db(response)

    return response["response"]


def refresh_token(user_id):
    revoke_old_refresh_token(user_id)

    response = authentication.refresh_token(user_id)

    save_data_token_in_db(response)

    return response["response"]


def revoke_token(token_id):
    token_data = auth_repository.get_by_jti(token_id)
    response = authentication.set_revoke_token(token_data)
    
    auth_repository.update_revoke(token_id, response["token_data"])

    return jsonify(response["is_disconnected"])


def is_token_revoked(token_id):
    token_data = auth_repository.get_by_jti(token_id)

    return authentication.check_is_token_revoked(token_data)


def save_data_token_in_db(response):
    access_token_data = authentication.create_data_token(response["access_token"],
                                   app.config["JWT_IDENTITY_CLAIM"])
    refresh_token_data = authentication.create_data_token(response["refresh_token"],
                                   app.config["JWT_IDENTITY_CLAIM"])
    auth_repository.save_data_tokens([access_token_data, refresh_token_data])


def revoke_old_refresh_token(user_id):
    old_refresh_token = auth_repository.get_non_revoked_refresh_token(user_id)

    if old_refresh_token:
        revoke_token(old_refresh_token["jti"])


# Verifica se o token foi revogado
@jwt.token_in_blacklist_loader
def token_in_blacklist_loader(decoded_token):
    jti = decoded_token["jti"]

    return is_token_revoked(jti)


def generate_verify_code():
    # TODO: Adicionar blacklist para descartar
    #  códigos pouco seguros, ex: 111111
    return random.sample(range(100000, 999999), 1)[0]


def generate_zenvia_payload (phone, verify_code):
    payload = {
        "from": "lookmix",
        "to": phone,
        "contents": [
            {
                "type": "text",
                "text": "Lookmix: Não compartilhe este dado com ninguém. "
                        "Seu código de verificação é %s" % verify_code
            }
        ]
    }
    return payload


def send_verify_code(payload):
    uri = "https://api.zenvia.com/v2/channels/sms/messages"

    response = requests.post(uri, data=payload)

    return response


def generate_OTP_jwt(sms_id, verify_code):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=80)

    encoded = jwt.encode(
        {
            "smsId": sms_id,
            "exp": expiration
        },
        verify_code,
        algorithms=[JWT_ALG])

    return encoded


def handle_OTP(phone):
    verify_code = generate_verify_code()

    payload_zenvia = generate_zenvia_payload(phone, verify_code)

    response = send_verify_code(payload_zenvia)

    status_code = response.status_code

    data = response.json()

    if status_code == 200:
        sms_id = data["id"]

        otp_jwt = generate_OTP_jwt(sms_id, verify_code)

        return jsonify({"verify_token": otp_jwt})
    return jsonify({"error": data["details"]["message"]})


def verify_code(token, code):
    attempts = 3

    try:
        jwt.decode(token, code, algorithms=[JWT_ALG])

        return jsonify({"is_valid": True})
    except jwt.ExpiredSignatureError:
        return jsonify({"is_valid": False, "error": "Code has been expirated"})
    except jwt.InvalidSignatureError:
        attempts = attempts - 1
        return jsonify({"is_valid": False, "attempts": attempts, "error": "Invalid code"})
