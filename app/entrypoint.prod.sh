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

mkdir -p $HOME/midata/private/static_volume
mkdir -p $HOME/midata/private/media_volume
mkdir -p $HOME/midata/private/esdata
mkdir -p $HOME/midata/private/postgres_data
chown -R 1000:1000 $HOME/midata/private

# prevents access denied error during collect static while creating static_volume/staticfiels/admin/ dir:
chmod -R a+w $HOME/midata/private/static_volume
echo "Running entrypoint.prod.sh ..."

exec "$@"
