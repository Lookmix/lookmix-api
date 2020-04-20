import flask
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from flask_jwt_extended import JWTManager
import nexmo


app = Flask(__name__)

# TODO: colocar em um arquivo .env
client = MongoClient("mongodb+srv://hanger:h4n6%26r.%40pp@cluster-xslqb.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client['hanger']
client_nexmo = nexmo.Client(key='c40c2038', secret='zbnV7nN9AfmshWN1')
app.secret_key = "@n6ul4r"
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

# TODO: mudar para True em produção
app.config['JWT_COOKIE_SECURE'] = False

app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_COOKIE_SAMESITE'] = 'Lax'
app.config['JWT_SESSION_COOKIE'] = False
# app.config['JWT_COOKIE_DOMAIN'] = 'lookmix.app'

jwt = JWTManager(app)
app_blueprint = flask.Blueprint("blueprint", __name__)
CORS(app_blueprint, supports_credentials=True)


from app.controllers import user_controller
from app.controllers import file_controller
from app.controllers import auth_controller

