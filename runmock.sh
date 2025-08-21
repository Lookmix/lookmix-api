#!/usr/lib/python3.7

source apivenv/bin/activate

export FLASK_APP=app.application:flask_mock_api
export FLASK_ENV=testing
export FLASK_DEBUG=True
export FLASK_RUN_HOST=127.10.10.10
export FLASK_RUN_PORT=5001
export ENVVAR_FILE=./../../.env.cfg

flask run