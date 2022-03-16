import flask
from flask import Flask
from datetime import datetime, timedelta
from jwt import encode
import uuid


app = Flask(__name__)

@app.route("/services/send-sms", methods=['POST'])
def zenvia_send_sms():
  return {}, 200


@app.route("/auth/get_otp", methods=['GET'])
def get_otp():
  expiration = datetime.utcnow() + timedelta(seconds=80)
  sms_id = str(uuid.uuid4())

  otp_jwt = encode(
    {
      "smsId": sms_id,
      "exp": expiration
    },
    str(000000),
    algorithm="HS256")

  return {
    "verify_token": otp_jwt, 
    "id": sms_id
  }, 200
