import flask
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# TODO: move to .env file
client = MongoClient("mongodb+srv://hanger:h4n6%26r.%40pp@cluster.xslqb.gcp.mongodb.net/db?retryWrites=true&w=majority")
db = client['db']

# TODO: move to .env file
app.config["JWT_SECRET_KEY"] = "CyFGMMt49gq4YZe" # app.secret_key = "CyFGMMt49gq4YZe"
app.config['JWT_COOKIE_SECURE'] = False # TODO: True in prod
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_COOKIE_SAMESITE'] = 'Lax'
app.config['JWT_COOKIE_DOMAIN'] = 'lookmix.app'
app.config['JWT_SESSION_COOKIE'] = False

jwt = JWTManager(app)
app_blueprint = flask.Blueprint("blueprint", __name__)
CORS(app_blueprint, supports_credentials=True)


from app.controllers import user_controller
from app.controllers import file_controller
from app.controllers import auth_controller

