from flask import Flask, request
from flask_jwt_extended import JWTManager
from werkzeug.middleware.proxy_fix import ProxyFix

application = Flask(__name__)
application.config.from_object("app.config")
application.config.from_envvar("ENVVAR_FILE")

jwt_manager = JWTManager(application)

from app.services.integrations import mongodb

db = mongodb.db_client

from app.controllers import auth_controller
from app.controllers import user_controller
from app.controllers import clothe_controller
from app.controllers import category_controller
from app.controllers import util_controller
from app.controllers import occasion_controller
from app.controllers import look_controller
from app.controllers import season_controller
from app.mock import mockapi

application.register_blueprint(auth_controller.bp)
application.register_blueprint(user_controller.bp)
application.register_blueprint(clothe_controller.bp)
application.register_blueprint(category_controller.bp)
application.register_blueprint(util_controller.bp)
application.register_blueprint(occasion_controller.bp)
application.register_blueprint(look_controller.bp)
application.register_blueprint(season_controller.bp)

flask_mock_api = mockapi.app
mock_jwt_manager = JWTManager(flask_mock_api)

# CORS config
@application.after_request
@flask_mock_api.after_request
def set_headers(response):
    allowed_origins = application.config.get("ALLOWED_ORIGINS")
    allowed_origin = allowed_origins[0]
    host_url = request.host_url[:-1]
    if host_url in allowed_origins:
        allowed_origin = host_url
    response.headers["Access-Control-Allow-Origin"] = allowed_origin
    response.headers["Access-Control-Allow-Headers"] = "content-type, X-CSRF-TOKEN"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    return response

application.wsgi_app = ProxyFix(
    application.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)