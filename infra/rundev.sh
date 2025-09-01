#!/usr/lib/python3.7

source ./../apivenv/bin/activate

export FLASK_APP=./../app.application
export FLASK_ENV=development
export FLASK_DEBUG=True
export FLASK_RUN_HOST=127.10.10.10
export FLASK_RUN_PORT=5000
export ENVVAR_FILE=./../infra/.env.cfg

flask run