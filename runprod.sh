#!/usr/lib/python3.7

source apivenv/bin/activate

export FLASK_APP=app.application
export FLASK_ENV=production
export FLASK_DEBUG=False
export ENVVAR_FILE=.env.prod.cfg

gunicorn -w 4 --access-logfile=- "app.application"