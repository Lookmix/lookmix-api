import flask
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from flask_jwt_extended import JWTManager


app = Flask(__name__)

# TODO: colocar em um arquivo .env
client = MongoClient("mongodb+srv://hanger:h4n6%26r.%40pp@cluster-xslqb.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client['hanger']
app.secret_key = "@n6ul4r"
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

CORS(app)
jwt = JWTManager(app)
app_blueprint = flask.Blueprint("blueprint", __name__)


from app.controllers import user_controller
from app.controllers import file_controller
from app.controllers import auth_controller
