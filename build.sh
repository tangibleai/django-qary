#!/usr/bin/env bash
echo "STOPPING ALL CONTAINERS!!!"
docker-compose down -v --remove-orphans


if [ "$1" == 'prod' ]
then
    echo "Building !PROD! docker image ..."
    docker-compose -f docker-compose.prod.yml up -d --build
    docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --no-input
    echo "Starting PROD containers for the webapp at http://localhost/ ..."
    docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
else
    echo "Building development docker image ..."
    docker-compose -f docker-compose.yml up -d --build
    docker-compose -f docker-compose.yml exec web python manage.py migrate --no-input
    echo "Starting development containers for the webapp at http://localhost:8000/ ..."
    docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear
fi
