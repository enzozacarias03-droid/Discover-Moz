#!/bin/sh
#Shell will terminate the execution of a script
#when a command fails


set -e


/scripts/wait_psql.sh
/scripts/collectstatic.sh
/scripts/makemigrations.sh
/scripts/migrate.sh
python manage.py createsuperuser --noinput || true
/scripts/runserver.sh