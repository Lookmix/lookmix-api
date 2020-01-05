# from 'módulo' import 'variável'
from app import app
from ..flickr_service import *
import json


@app.route("/upload", methods=['POST'])
def upload_file():
    response = upload()
    return json.dumps(response.__dict__), 200

