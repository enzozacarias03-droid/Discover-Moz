#!/bin/sh

echo ">>> Step 1: Waiting for DB..."
/scripts/wait_psql.sh || { echo "FAILED: wait_psql"; exit 1; }

echo ">>> Step 2: Collecting static files..."
/scripts/collectstatic.sh || { echo "FAILED: collectstatic"; exit 1; }

echo ">>> Step 3: Running migrate..."
python manage.py migrate --noinput 2>&1 || { echo "FAILED: migrate"; exit 1; }

echo ">>> Step 4: Creating superuser..."
python manage.py createsuperuser --noinput 2>&1 || true

echo ">>> Step 5: Starting gunicorn on port ${PORT:-8000}..."
exec gunicorn project.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers 2 \
  --timeout 120 \
  --log-level debug 2>&1