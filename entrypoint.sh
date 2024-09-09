#!/bin/sh

# Run Django migrations and collect static files
python manage.py migrate
python manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8001
