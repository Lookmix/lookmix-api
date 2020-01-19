from flask import Flask
import flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app_blueprint = flask.Blueprint("blueprint", __name__)


from app.controllers import user_controller
from app.controllers import file_controller
