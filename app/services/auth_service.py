from app import app #, jwt
from flask import jsonify
from app.repositories import auth_repository, user_repository
import requests
import jwt
import random
from datetime import datetime, timedelta
import uuid
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from bson.objectid import ObjectId
from app.exceptions.error import (
    BadCredentialsException
)

JWT_ALG = "HS256"
# TODO: colocar em um arquivo de constants
expires_access_token = timedelta(minutes=30)
expires_refresh_token = timedelta(days=2)


def attempt_login(request_data):
    user = user_repository.get_by_phone(request_data["phone"])

    if user and check_password_hash(user["password"], request_data["password"]):
        user_id = str(ObjectId(user["_id"]))

        response = create_tokens(user_id)

        save_auth_metadata(response)

        return response["data"]
    else:
        raise BadCredentialsException()


def create_tokens(user_id):
    access_token = create_access_token(identity=user_id,
                                       expires_delta=expires_access_token,
                                       fresh=True)
    refresh_token = create_refresh_token(user_id,
                                         expires_delta=expires_refresh_token)
    decoded_access_token = decode_token(access_token)
    decoded_refresh_token = decode_token(refresh_token)
    
    response = jsonify({
        "access_metadata": {
            "expires": datetime.datetime.fromtimestamp(decoded_access_token["exp"]),
            "jti": decoded_access_token["jti"]
        },
        "refresh_metadata": {
            "expires": datetime.datetime.fromtimestamp(decoded_refresh_token["exp"]),
            "jti": decoded_refresh_token["jti"]
        }
    })
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return {
        "data": response,
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def refresh_token(user_id):
    # revoke_old_refresh_token(user_id)

    response = create_tokens(user_id)

    save_auth_metadata(response)

    return response["data"]

# Remove from cookie
def revoke_token(): # token_id):
    response = {"is_disconnected": True}

    unset_jwt_cookies(jsonify(response))
    
    return jsonify(response["is_disconnected"])


def save_auth_metadata(response):
    access_metadata = create_auth_metadata(response["access_token"],
                                   app.config["JWT_IDENTITY_CLAIM"])
    refresh_metadata = create_auth_metadata(response["refresh_token"],
                                   app.config["JWT_IDENTITY_CLAIM"])
    auth_repository.save_many_auth_metadata([access_metadata, refresh_metadata])


def create_auth_metadata(encoded_token, identity_claim):
    decoded_token = decode_token(encoded_token)

    data_token = {
        "jti": decoded_token["jti"],
        "timestamp": datetime.now(),
        # "token_type": decoded_token["type"],
        "user_id": decoded_token[identity_claim],
        # "expires": datetime.datetime.fromtimestamp(decoded_token["exp"]),
        # "revoked": False,
    }
    return data_token


def generate_verify_code():
    # TODO: Adicionar blacklist para descartar
    #  códigos pouco seguros, ex: 111111
    # return 123456
    return random.sample(range(100000, 999999), 1)[0]


def generate_zenvia_payload (phone, verify_code):
    schedule = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    payload = {
        "sendSmsRequest": {
            "from": "Lookmix",
            "to": "55%s" % phone,
            "schedule": schedule,
            "msg": "Lookmix: Não compartilhe este dado com ninguém. Seu código de verificação é %s" % verify_code,
            "callbackOption": "NONE",
            "id": uuid.uuid4(),
            "flashSms": False
        }
    }
    return payload


def send_verify_code(payload):
    uri = "https://api-rest.zenvia.com/services/send-sms"

    headers = {
        "Authorization": "Basic dmluaWNpdXMub3RhdmlvLnNtczo0TmF4cko0NURY",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.post(uri, data=payload, headers=headers)

    return response


def generate_OTP_jwt(sms_id, verify_code):
    expiration = datetime.utcnow() + timedelta(seconds=80)

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

    if status_code == 201:
        sms_id = data["id"]

        otp_jwt = generate_OTP_jwt(sms_id, verify_code)

        save_OTP_meta(sms_id, phone)

        return jsonify({"verify_token": otp_jwt})
    return jsonify({"error": data["details"]["message"]})


def verify_code(token, code):
    try:
        jwt.decode(token, code, algorithms=[JWT_ALG])

        return jsonify({"is_valid": True})
    except jwt.ExpiredSignatureError:
        return jsonify({"is_valid": False, "error": "Code has been expirated"})
    except jwt.InvalidSignatureError:
        update_OTP_attempts()
        return jsonify({"is_valid": False, "error": "Invalid code"})


def save_OTP_meta(id, phone):
    otp_meta = {
        "attempts": 0,
        "id": id,
        "phone": phone,
        "timestamp": datetime.now(),
        "expires": set_otp_expires_time()
    }
    auth_repository.save_otp_metadata(otp_meta)
    return otp_meta


def update_OTP_attempts(id):
    auth_repository.increment_otp_attempts(id)


def set_otp_expires_time():
    timestamp = datetime.now()
    date = timestamp.date()
    day = date.day
    month = date.month
    year = date.year
    time = timestamp.time()
    hour = time.hour
    minutes = time.minute + 1
    seconds = time.second + 35
    expires_timedelta = timedelta(hours=hour, minutes=minutes, seconds=seconds)
    result = str(expires_timedelta).split(", ")
    index = 0

    if len(result) == 2:
        index = 1
    return "%s-%s-%s %s" % (year, month, day, result[index])