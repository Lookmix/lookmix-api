from flask import Flask, request
from datetime import datetime, timedelta
from jwt import encode
import uuid
from app.services import auth_service

app = Flask(__name__)

@app.route("/services/send-sms", methods=['POST'])
def zenvia_send_sms():
  return {}, 200


@app.route("/auth/get_otp", methods=['GET'])
def get_otp():
  phone = request.args.get("phone")

  expiration = datetime.utcnow() + timedelta(seconds=80)
  sms_id = str(uuid.uuid4())

  otp_jwt = encode(
    {
      "smsId": sms_id,
      "exp": expiration
    },
    str(111111),
    algorithm="HS256")

  auth_service.save_otp_meta(sms_id, phone)

  return {
    "token": otp_jwt, 
    "id": sms_id
  }, 200
