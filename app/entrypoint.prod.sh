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

# prevents access denied error during collect static while creating static_volume/staticfiels/admin/ dir:
chmod -R a+w $HOME/midata/private/static_volume
echo "Running entrypoint.prod.sh ..."

exec "$@"
