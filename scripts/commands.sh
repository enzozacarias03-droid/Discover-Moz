#!/bin/sh
set -e

echo ">>> Step 1: Waiting for DB..."
/scripts/wait_psql.sh

echo ">>> Step 2: Collecting static files..."
/scripts/collectstatic.sh

echo ">>> Step 3: Running migrate..."
python manage.py migrate --noinput

echo ">>> Step 4: Creating superuser..."
python manage.py createsuperuser --noinput || true

echo ">>> Step 5: Starting gunicorn on port ${PORT:-8000}..."
exec gunicorn project.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers 2 \
  --timeout 120 \
  --log-level info