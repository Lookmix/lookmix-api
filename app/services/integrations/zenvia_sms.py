import requests
from bson.json_util import dumps
import uuid
from app.application import application

def send_sms(payload):
    uri = application.config("ZENVIA_URI")
    security = application.config("ZENVIA_SECURITY")

    headers = {
        "Authorization": f"Basic {security}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.post(uri, data=payload, headers=headers)

    return response

def generate_zenvia_payload (phone, schedule, msg):
    payload = {
        "sendSmsRequest": {
            "from": "Lookmix",
            "to": f"55{phone}",
            "schedule": schedule,
            "msg": msg,
            "callbackOption": "NONE",
            "id": str(uuid.uuid4()),
            "flashSms": False
        }
    }
    return dumps(payload)
