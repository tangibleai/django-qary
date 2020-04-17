#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for $DATABASE..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.27
    done

    echo "PostgreSQL started"
fi

echo "Running entrypoint.prod.sh ..."

# python manage.py flush --no-input
# python manage.py migrate
# python manage.py collectstatic --no-input --clear

exec "$@"
