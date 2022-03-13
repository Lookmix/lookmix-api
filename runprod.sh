#!/usr/lib/python3.7

export FLASK_APP=app
export FLASK_ENV=production
export FLASK_DEBUG=False
export FLASK_HOST=api.lookmix.app
export FLASK_PORT=5000
export ENVVAR_FILE=./../../.env

flask run