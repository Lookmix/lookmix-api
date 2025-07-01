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
    unset_jwt_cookies,
    set_access_cookies,
    set_refresh_cookies, 
)
from bson.json_util import loads
from app import app #, jwt
from app.exceptions.error import (
    BadCredentialsException,
    FailToGenerateOTPException,
    AttemptsExceedException
)
from app.repositories import (
    auth_repository, 
    user_repository
)
from app.utils import validation
from app.services.integrations.zenvia_sms import (
    generate_zenvia_payload, 
    send_sms
)
from app.services.integrations.emailjs import (
    generate_emailjs_otp_payload, 
    send_email
)

JWT_ALG = "HS256"
expires_access_token = timedelta(minutes=30)
expires_refresh_token = timedelta(days=2)


def validate_credentials(request_data):
    validate_login_data_model(request_data)
    phone = request_data.get("phone")
    request_password = request_data.get("password")
    user = user_repository.get_by_phone(phone)
    if user is not None:
        db_password = user.get("password")
        is_password_valid = check_password_hash(db_password, request_password)
        if is_password_valid:
            user_id = user.get("_id")
            return user_id
    raise BadCredentialsException()


def create_tokens(user_id):
    access_token = create_access_token(identity=user_id,
                                       expires_delta=expires_access_token)
    refresh_token = create_refresh_token(identity=user_id,
                                         expires_delta=expires_refresh_token)
    decoded_access_token = decode_token(access_token)
    decoded_refresh_token = decode_token(refresh_token)
    response = {
        "access_metadata": {
            "expires": datetime.fromtimestamp(decoded_access_token["exp"]),
            "jti": decoded_access_token["jti"]
        },
        "refresh_metadata": {
            "expires": datetime.fromtimestamp(decoded_refresh_token["exp"]),
            "jti": decoded_refresh_token["jti"]
        }
    }
    return {
        "data": response,
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def handle_tokens(user_id):
    tokens = create_tokens(user_id)
    access = tokens.get("access_token")
    refresh = tokens.get("refresh_token")
    auth_metadata = tokens.get("data")
    response = {}
    response["auth"] = auth_metadata
    save_auth_metadata(access)
    save_auth_metadata(refresh)
    response = jsonify(response)
    set_access_cookies(response, access)
    set_refresh_cookies(response, refresh)
    return response


# Remove from cookie
def revoke_token(): # token_id):
    response = {"is_disconnected": True}
    response = jsonify(response)
    unset_jwt_cookies(response)
    return response


def save_auth_metadata(encoded_token, is_reset_password_token=False, is_new_user_token=False):
    decoded_token = decode_token(encoded_token)
    metadata = {
        "jti": decoded_token["jti"],
        "timestamp": datetime.now(),
        "token_type": decoded_token["type"],
        "is_reset_password_token": is_reset_password_token,
        "is_new_user_token": is_new_user_token
        # "expires": datetime.datetime.fromtimestamp(decoded_token["exp"]),
        # "revoked": False,
    }
    auth_repository.save_auth_metadata(metadata)


def generate_otp():
    # TODO: add blacklist to avoid codes like 111111
    return random.sample(range(100000, 999999), 1)[0]


def generate_otp_jwt(id, otp):
    expiration = datetime.utcnow() + timedelta(seconds=80)
    encoded = encode(
        {
            "id": id,
            "exp": expiration
        },
        str(otp), # secret
        algorithm=JWT_ALG
    )
    return encoded


# uses zenvia/sms to send otp
def handle_otp(phone):
    otp = generate_otp()
    schedule = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    msg = "Nao compartilhe este dado com ninguem. Seu codigo de verificacao é %s" % otp
    payload_zenvia = generate_zenvia_payload(phone, schedule, msg)
    response = send_sms(payload_zenvia)
    status_code = response.status_code
    data = response.json()
    if status_code == 201 or status_code == 200:
        payload_zenvia = loads(payload_zenvia)
        sms_id = payload_zenvia.get("sendSmsRequest", {}).get("id", None)
        otp_jwt = generate_otp_jwt(sms_id, otp)
        save_otp_meta(sms_id, phone=phone)
        return jsonify({
            "token": otp_jwt, 
            "id": sms_id
        })
    error_message = data.get("exception", {}).get("message", {})
    raise FailToGenerateOTPException(error_message)


# uses emailjs/email to send otp
def handle_otp2(to_email, to_name=None):
    otp = generate_otp()
    payload_emailjs = generate_emailjs_otp_payload(to_email, to_name, otp)
    response = send_email(payload_emailjs)
    status_code = response.status_code
    # data = response.json()
    # print(data)
    print(response.text)
    if status_code == 200:
        # payload_emailjs = loads(payload_emailjs)
        email_id = str(uuid.uuid4()) # data.get("id", None)
        otp_jwt = generate_otp_jwt(email_id, otp)
        save_otp_meta(email_id, email=to_email)
        return jsonify({
            "token": otp_jwt,
            "id": email_id
        })
    error_message = "Fail" # data.get("exception", {}).get("message", {})
    raise FailToGenerateOTPException(error_message)


def verify_otp(data):
    validate_otp_data_model(data)
    token = data.get("token")
    code = data.get("code")
    id = data.get("id")
    try:
        attemps = get_otp_attempts(id)
        if attemps > 2:
            raise AttemptsExceedException()
        decode(token, code, algorithms=[JWT_ALG])
        return { "valid": True }
    except InvalidSignatureError:
        update_otp_attempts(id)
        attemps = get_otp_attempts(id)
        if attemps > 2:
            raise AttemptsExceedException()
        raise InvalidSignatureError


def save_otp_meta(id, phone=None, email=None):
    otp_meta = {
        "attempts": 0,
        "_id": id,
        "phone": phone,
        "email": email,
        "timestamp": datetime.now(),
        "expires": generate_otp_expires_time()
    }
    auth_repository.save_otp_metadata(otp_meta)
    return otp_meta


def get_otp_attempts(id):
    return auth_repository.get_otp_attempts(id)


def update_otp_attempts(id):
    auth_repository.increment_otp_attempts(id)


def generate_otp_expires_time():
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


def validate_otp_data_model(otp_data_model):
    validation.assert_valid_schema(otp_data_model, "otp.json")


def validate_login_data_model(login_data_model):
    validation.assert_valid_schema(login_data_model, "login.json")
