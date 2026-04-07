#!/bin/sh
set -e

echo "========================================="
echo ">>> Container started at: $(date)"
echo ">>> Environment check:"
echo "    PORT=${PORT}"
echo "    DEBUG=${DEBUG}"
echo "    ALLOWED_HOSTS=${ALLOWED_HOSTS}"
echo "    POSTGRES_HOST=${POSTGRES_HOST}"
echo "    POSTGRES_PORT=${POSTGRES_PORT}"
echo "    POSTGRES_DB=${POSTGRES_DB}"
echo "========================================="

echo ">>> Step 1: Waiting for DB..."
/scripts/wait_psql.sh
echo ">>> DB is ready."

echo ">>> Step 2: Collecting static files..."
python manage.py collectstatic --noinput --clear
echo ">>> Static files collected."

echo ">>> Step 3: Running migrate..."
python manage.py migrate --noinput
echo ">>> Migrations done."

echo ">>> Step 4: Creating superuser (errors are OK here)..."
python manage.py createsuperuser --noinput 2>&1 || echo ">>> Superuser already exists or skipped."

echo ">>> Step 5: Starting gunicorn on port ${PORT:-8000}..."
exec gunicorn project.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers 2 \
  --timeout 120 \
  --log-level debug \
  --access-logfile - \
  --error-logfile -