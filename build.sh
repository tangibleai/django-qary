#!/usr/bin/env bash
set -e

echo "STOPPING ALL CONTAINERS!!!"
docker-compose down -v --remove-orphans
echo

if [ "$1" == 'prod' ]
then
    echo "removing 'midata' docker volume"
    docker volume rm -f midata
    echo

    echo "Building PROD docker image ..."
    docker-compose -f docker-compose.prod.yml up -d --build
    echo

    echo "Migrating PROD db ..."
    docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --no-input
    echo

    echo "Starting PROD containers for the webapp at http://localhost/ ..."
    docker-compose -f docker-compose.prod.yml exec -v /midata:/home/app/web/midata:ro web python manage.py collectstatic --no-input --clear
    echo
else
    echo "Building development docker image ..."
    docker volume rm -f midata
    docker-compose -f docker-compose.yml up -d --build
    docker-compose -f docker-compose.yml exec web python manage.py migrate --no-input
    echo "Starting development containers for the webapp at http://localhost:8000/ ..."
    docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear
fi
