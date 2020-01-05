# from 'módulo' import 'variável'
from app import app
import json


@app.route("/")
def getAll():
    return json.dumps(['Camiseta', 'Calca', 'Tenis']), 200
