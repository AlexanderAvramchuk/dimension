#!/bin/bash

NAME="dimension"                                  # Name of the application
DJANGODIR=/projects/dimension/project/            # Django project directory
SOCKFILE=/projects/dimension/socket/dimension.sock
USER=prog                                       # the user to run as
                                    # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=dimension.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=dimension.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /projects/dimension/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /projects/dimension/venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER \
  --bind=unix:$SOCKFILE \
  --log-level=error \
  --log-file=-
  --timeout=90
  --graceful-timeout=10
