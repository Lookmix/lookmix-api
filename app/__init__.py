from flask import Flask, request
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object("app.config")
app.config.from_envvar("ENVVAR_FILE")

jwt_manager = JWTManager(app)

from app.services.integrations import mongodb

db = mongodb.db_client

from app.controllers import auth_controller
from app.controllers import user_controller
from app.controllers import clothe_controller
from app.controllers import category_controller
from app.controllers import util_controller
from app.controllers import occasion_controller
from app.controllers import look_controller
from app.mock import mockapi

app.register_blueprint(auth_controller.bp)
app.register_blueprint(user_controller.bp)
app.register_blueprint(clothe_controller.bp)
app.register_blueprint(category_controller.bp)
app.register_blueprint(util_controller.bp)
app.register_blueprint(occasion_controller.bp)
app.register_blueprint(look_controller.bp)

flask_mock_api = mockapi.app
mock_jwt_manager = JWTManager(flask_mock_api)

# CORS config
@app.after_request
@flask_mock_api.after_request
def set_headers(response):
    allowed_origins = app.config.get("ALLOWED_ORIGINS")
    allowed_origin = allowed_origins[0]
    host_url = request.host_url[:-1]

    if host_url in allowed_origins:
        allowed_origin = host_url

    response.headers["Access-Control-Allow-Origin"] = allowed_origin
    response.headers["Access-Control-Allow-Headers"] = "content-type"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response
