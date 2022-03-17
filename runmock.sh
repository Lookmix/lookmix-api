#!/usr/lib/python3.7

export FLASK_APP=app:flask_mock_api
export FLASK_ENV=testing
export FLASK_DEBUG=True
export FLASK_RUN_HOST=127.0.0.1
export FLASK_RUN_PORT=5001
export ENVVAR_FILE=./../../.env.cfg

flask run