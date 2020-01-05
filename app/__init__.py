from flask import Flask


app = Flask(__name__)


from app.controllers import user_controller
from app.controllers import file_controller
