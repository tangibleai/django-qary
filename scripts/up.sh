#!/usr/bin/env bash
set -e

echo ''
if [ "$1" == 'prod' ]
then
    MIDATA_HOST_PATH=/midata/public
    mkdir -p $MIDATA_HOST_PATH

    echo "STOPPING ALL CONTAINERS!!!"
    docker-compose down -v --remove-orphans

    echo ''
    echo "Building !PROD! docker image ..."
    docker-compose -f docker-compose.prod.yml up -d
    docker-compose -f docker-compose.prod.yml exec web python manage.py migrate upload --no-input

    echo ''
    echo "Starting PROD containers for the webapp at http://localhost/ ..."
    docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic upload --no-input --clear
elif [ "$1" == 'dev' ]
then
    MIDATA_HOST_PATH="$HOME/midata/public"
    mkdir -p $MIDATA_HOST_PATH

    echo "STOPPING ALL CONTAINERS!!!"
    docker-compose down -v --remove-orphans

    echo ''
    echo "Building development docker image with nginx path=$MIDATA_HOST_PATH ..."
    docker-compose -f docker-compose.dev.yml up -d
    docker-compose -f docker-compose.def.yml exec web python manage.py migrate upload --no-input

    echo ''
    echo "Starting development containers for the webapp at http://localhost:8000/ ..."
    docker-compose -e MIDATA_HOST_PATH=$MIDATA_HOST_PATH -f docker-compose.dev.yml exec web python manage.py collectstatic --no-input --clear
elif [ "$1" == 'stop' ]
then
    echo "STOPPING ALL CONTAINERS!!!"
    docker-compose down -v --remove-orphans
fi
