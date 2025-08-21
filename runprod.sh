#!/usr/lib/python3.7

source apivenv/bin/activate

export FLASK_APP=app.application
export FLASK_ENV=production
export FLASK_DEBUG=False
export FLASK_RUN_HOST=api.lookmix.app
export FLASK_RUN_PORT=80
export ENVVAR_FILE=./../../.env.prod.cfg

flask run