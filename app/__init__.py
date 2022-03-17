from flask import Flask
from pymongo import MongoClient
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('app.config')
app.config.from_envvar('ENVVAR_FILE')
# print(f" * HEALTH-CHECK-ENV-VAR: {app.config.get('HEALTH')}")
jwt_manager = JWTManager(app)

mongodb_url = app.config.get("MONGODB_HOST")
client = MongoClient(mongodb_url)
db = client['db']

from app.controllers import auth_controller
from app.controllers import user_controller
from app.controllers import file_controller
from app.mock import mockapi

app.register_blueprint(auth_controller.bp)
app.register_blueprint(user_controller.bp)
app.register_blueprint(file_controller.bp)

flask_mock_api = mockapi.app
mock_jwt_manager = JWTManager(flask_mock_api)

# CORS config
@app.after_request
@flask_mock_api.after_request
def set_allowed_origin_header(response):
  origin = app.config.get("ALLOWED_ORIGIN")
  response.headers["Access-Control-Allow-Origin"] = origin
  response.headers["Access-Control-Allow-Headers"] = 'content-type'
  return response
