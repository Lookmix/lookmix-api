# from 'módulo' import 'variável'
from app import app, app_blueprint
import flickr_api
import json
from services import flickr_service, user_service


@app_blueprint.route("/get_user", methods=['GET'])
def get_user():
    # flickr_service.set_auth_handler()
    user = user_service.get_user()
    return json.dumps(user.__dict__), 200
    # return json.dumps(['Camiseta', 'Calca', 'Tenis']), 200


@app_blueprint.route("/get_photos", methods=['GET'])
def get_photos():
    # flickr_service.set_auth_handler()
    photos = user_service.get_photos()
    return json.dumps(photos), 200


app.register_blueprint(app_blueprint, url_prefix="/api")