# from 'módulo' import 'variável'
from app import app, app_blueprint
import json


@app_blueprint.route("/", methods=['GET'])
def get_all_users():
    return json.dumps(['Camiseta', 'Calca', 'Tenis']), 200


app.register_blueprint(app_blueprint, url_prefix="/api")