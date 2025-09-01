#!/usr/lib/python3.7

source ./../apivenv/bin/activate

export FLASK_ENV=production
export FLASK_DEBUG=False
export ENVVAR_FILE=
export ENVVAR_FILE=./../infra/.env.prod.cfg

PYTHONPATH=.. gunicorn -w 4 --access-logfile=- "app.application"