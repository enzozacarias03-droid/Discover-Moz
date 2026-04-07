#!/bin/sh
set -e

echo ">>> Step 1: Waiting for DB..."
/scripts/wait_psql.sh

echo ">>> Step 2: Collecting static files..."
/scripts/collectstatic.sh

echo ">>> Step 3: Running makemigrations..."
python manage.py makemigrations --noinput

echo ">>> Step 4: Running migrate..."
python manage.py migrate --noinput

echo ">>> Step 5: Creating superuser..."
python manage.py createsuperuser --noinput || true

echo ">>> Step 6: Starting gunicorn..."
gunicorn project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120