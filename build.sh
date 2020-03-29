#!/usr/bin/env bash
set -e

echo ''
if [ "$1" == 'prod' ]
then
    echo "STOPPING ALL CONTAINERS!!!"
    docker-compose down -v --remove-orphans

    echo ''
    echo "Building !PROD! docker image ..."
    docker-compose -f docker-compose.prod.yml up -d --build
    docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --no-input

    echo ''
    echo "Starting PROD containers for the webapp at http://localhost/ ..."
    docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
elif [ "$1" == 'dev' ]
then
    echo "STOPPING ALL CONTAINERS!!!"
    docker-compose down -v --remove-orphans

    echo ''
    echo "Building development docker image ..."
    docker-compose -f docker-compose.yml up -d --build
    docker-compose -f docker-compose.yml exec web python manage.py migrate --no-input

    echo ''
    echo "Starting development containers for the webapp at http://localhost:8000/ ..."
    docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear
elif [ "$1" == 'stop' ]
then
    echo "STOPPING ALL CONTAINERS!!!"
    docker-compose down -v --remove-orphans
fi
