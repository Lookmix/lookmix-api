import requests
from bson.json_util import dumps
from app import app

__SERVICE_ID = "acc_service"
__ACC_CONFIRMATION_TEMPLATE_ID = "acc_confirmation"
__PASS_RESET_TEMPLATE_ID = "pass_reset"

def send_email(payload):
    emailjs_url = app.config.get("EMAILJS_URL")
    url = f"{emailjs_url}/email/send"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.post(url, data=payload, headers=headers)
    return response

def generate_password_reset_payload(to_email, to_name, code):
    payload = {
        "service_id": __SERVICE_ID,
        "template_id": __PASS_RESET_TEMPLATE_ID,
        "user_id": app.config.get("EMAILJS_USER_ID"),
        "template_params": {
            "to_email": to_email,
            "to_name": to_name,
            "from_name": "Lookmix",
            # "subject": "Redefinição de senha",
            "code": code
        }
    }
    return dumps(payload)

def generate_acc_confirmation_payload (to_email, to_name, code):
    payload = {
        "service_id": __SERVICE_ID,
        "template_id": __ACC_CONFIRMATION_TEMPLATE_ID,
        "user_id": app.config.get("EMAILJS_USER_ID"),
        "template_params": {
            "to_email": to_email,
            "to_name": to_name,
            "from_name": "Lookmix",
            # "subject": "Confirme seu e-mail",
            "code": code
        }
    }
    return dumps(payload)