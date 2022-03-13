import flask
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('app.config')
app.config.from_envvar('ENVVAR_FILE')

print(f" * HEALTH-CHECK-ENV-VAR: {app.config.get('HEALTH')}")

mongodb_url = app.config.get("MONGODB_HOST")

client = MongoClient(mongodb_url)
db = client['db']

jwt = JWTManager(app)
app_blueprint = flask.Blueprint("blueprint", __name__)
CORS(app_blueprint, supports_credentials=True)


from app.controllers import user_controller
from app.controllers import file_controller
from app.controllers import auth_controller

