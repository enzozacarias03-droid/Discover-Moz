#!/bin/sh
echo "BASE_DIR contents:"
ls /djangoapp/
echo "Blog static folder:"
ls /djangoapp/blog/static/blog/css/
python manage.py collectstatic --noinput --clear