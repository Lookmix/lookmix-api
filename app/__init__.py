import flask
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from flask_jwt import JWT
from bson.objectid import ObjectId
from werkzeug.security import check_password_hash


def authenticate(username, password):
    user = db['usuarios'].find_one({"username": username})

    if user and check_password_hash(user['password'], password):
        return user


def identity(payload):
    user_id = payload['identity']

    return db['usuarios'].find_one({"_id": ObjectId(user_id)})


app = Flask(__name__)
CORS(app)
client = MongoClient("mongodb+srv://hanger:h4n6%26r.%40pp@cluster-xslqb.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client['hanger']
app_blueprint = flask.Blueprint("blueprint", __name__)
app.secret_key = "@n6ul4r"
jwt = JWT(app, authenticate, identity)

from app.controllers import user_controller
from app.controllers import file_controller
