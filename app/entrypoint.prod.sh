#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for $DATABASE..."
    chown -R postgres "$PGDATA"

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.27
    done

    echo "PostgreSQL started"
fi


echo "Running entrypoint.prod.sh ..."

exec "$@"
