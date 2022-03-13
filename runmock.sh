#!/usr/lib/python3.7

export FLASK_APP=mock
export FLASK_ENV=development
export FLASK_DEBUG=True
export FLASK_HOST=127.0.0.1
export FLASK_PORT=5001
export ENVVAR_FILE=./../../.env.cfg

cd app/tests/ && flask run
