#!/bin/bash
if [ "$TYPE" = "django" ]
then
    #python /app/manage.py makemigrations
    python /app/manage.py migrate
    python /app/manage.py runserver 0.0.0.0:8000
else
    watchmedo auto-restart -d tasks -- celery -A tasks worker -l info
fi