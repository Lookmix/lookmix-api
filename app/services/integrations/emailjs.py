import requests
from bson.json_util import dumps
from app import app

__EMAILJS_SERVICE_ID = "acc_confirmation_service"
__EMAILJS_TEMPLATE_ID = "acc_confirmation"

def send_email(payload):
    emailjs_url = app.config.get("EMAILJS_URL")
    url = f"{emailjs_url}/email/send"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.post(url, data=payload, headers=headers)
    return response

def generate_emailjs_otp_payload (to_email, to_name, code):
    payload = {
        "service_id": __EMAILJS_SERVICE_ID,
        "template_id": __EMAILJS_TEMPLATE_ID,
        "user_id": app.config.get("EMAILJS_USER_ID"),
        "template_params": {
            "to_email": to_email,
            "to_name": to_name,
            "from_name": "Lookmix",
            "subject": "Confirme seu e-mail",
            "code": code
        }
    }
    return dumps(payload)