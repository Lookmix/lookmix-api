import requests
import random
import uuid

from jwt import (
    InvalidSignatureError, 
    decode, 
    encode
)
from flask import jsonify
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token, 
    set_access_cookies,
    set_refresh_cookies, 
    unset_jwt_cookies
)
from bson.objectid import ObjectId
from bson.json_util import (
    dumps,
    loads
)
from app import app #, jwt
from app.exceptions.error import (
    BadCredentialsException,
    FailToGenerateVerifyCodeException,
    AttemptsExceedException
)
from app.repositories import (
    auth_repository, 
    user_repository
)
from app.utils import validation
from app.services import user_service


JWT_ALG = "HS256"
# TODO: colocar em um arquivo de constantes
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
            "expires": datetime.fromtimestamp(decoded_access_token["exp"]),
            "jti": decoded_access_token["jti"]
        },
        "refresh_metadata": {
            "expires": datetime.fromtimestamp(decoded_refresh_token["exp"]),
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
    return random.sample(range(100000, 999999), 1)[0]


def generate_zenvia_payload (phone, verify_code):
    schedule = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    payload = {
        "sendSmsRequest": {
            "from": "Lookmix",
            "to": "55%s" % phone,
            "schedule": schedule,
            "msg": "Não compartilhe este dado com ninguém. Seu código de verificação é %s" % verify_code,
            "callbackOption": "NONE",
            "id": str(uuid.uuid4()),
            "flashSms": False
        }
    }
    return dumps(payload)


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

    encoded = encode(
        {
            "smsId": sms_id,
            "exp": expiration
        },
        str(verify_code),
        algorithm=JWT_ALG)
    return encoded


def handle_OTP(phone):
    verify_code = generate_verify_code()

    payload_zenvia = generate_zenvia_payload(phone, verify_code)

    response = send_verify_code(payload_zenvia)

    status_code = response.status_code

    data = response.json()

    if status_code == 201 or status_code == 200:
        payload_zenvia = loads(payload_zenvia)

        sms_id = payload_zenvia.get("sendSmsRequest", {}).get("id", None)

        otp_jwt = generate_OTP_jwt(sms_id, verify_code)

        save_OTP_meta(sms_id, phone)

        return jsonify({
            "verify_token": otp_jwt, 
            "id": sms_id
        })
    raise FailToGenerateVerifyCodeException(data.get("exception", {}).get("message", {}))

 
def verify_code(data):
    id = None

    try:
        user = data.get("user")

        if user is not None:
            user["timestamp"] = str(datetime.now())
            data["user"] = user

        validate_verify_token_data(data)

        token = data.get("token")
        code = data.get("code")
        id = data.get("id")

        decode(token, code, algorithms=[JWT_ALG])

        user_service.save(user)

        return jsonify({"valid": True})
    except InvalidSignatureError:
        update_OTP_attempts(id)

        attemps = get_OTP_attempts(id)

        if attemps > 2:
            raise AttemptsExceedException()
        raise InvalidSignatureError


def save_OTP_meta(id, phone):
    otp_meta = {
        "attempts": 0,
        "_id": id,
        "phone": phone,
        "timestamp": datetime.now(),
        "expires": set_otp_expires_time()
    }
    auth_repository.save_otp_metadata(otp_meta)
    return otp_meta


def get_OTP_attempts(id):
    return auth_repository.get_otp_attempts(id)


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


def validate_verify_token_data(verify_token_data):
    validation.assert_valid_schema(verify_token_data, "verify_token.json")

