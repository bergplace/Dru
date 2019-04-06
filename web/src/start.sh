#!/bin/bash

if [ "$DEBUG" = "true" ]
    then
        if [ "$TYPE" = "django" ]
            then
                python3 /app/manage.py migrate
                python3 /app/manage.py runserver 0.0.0.0:80
            else
                watchmedo auto-restart -d tasks -- celery -A web worker -l info
        fi
    else # production
        if [ "$TYPE" = "django" ]
            then
                python3 /app/manage.py migrate
                /usr/bin/supervisord -c /home/www-user/supervisord.conf &
                sleep infinity
            else
                celery -A web worker -l info
        fi
fi