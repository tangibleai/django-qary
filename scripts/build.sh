#!/usr/bin/env bash
set -e

echo ''
if [ "$1" == 'prod' ]
then
    MIDATA_HOST_PATH="$HOME/midata/public"
    mkdir -p $MIDATA_HOST_PATH

    echo "STOPPING ALL CONTAINERS!!!"
    docker-compose -f docker-compose.prod.yml down -v --remove-orphans

    echo ''
    echo "Bringing up docker-compose.prod.yml docker images ..."
    docker-compose -f docker-compose.prod.yml up -d --build

    echo "Migrating DB in PROD containers with exec web python manage.py migrate (without --no-input)"
    docker-compose  -f docker-compose.prod.yml exec --user app web python manage.py migrate

    echo ''
    echo "Collecting static in PROD containers for the webapp with exec web python manage.py collect static ..."
    docker-compose  -f docker-compose.prod.yml exec --user app web python manage.py collectstatic --no-input  # --clear

    echo "Indexing wikipedia categories and testing Elasticsearch"
    docker-compose  -f docker-compose.prod.yml exec --user app web python elastic_app/es_index.py
elif [ "$1" == 'dev' ]
then
    MIDATA_HOST_PATH="$HOME/midata/public"
    mkdir -p $MIDATA_HOST_PATH

    echo "STOPPING ALL CONTAINERS!!!"
    docker-compose -f docker-compose.dev.yml down -v --remove-orphans

    echo ''
    echo "Building development docker image with nginx path=$MIDATA_HOST_PATH ..."
    docker-compose -f docker-compose.dev.yml up -d --build
    echo "Running exec web python manage.py migrate (without --no-input)"
    docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

    echo ''
    echo "Starting development containers for the webapp at http://localhost:8000/ ..."
    docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --no-input --clear
elif [ "$1" == 'stop' ]
then
    echo "STOPPING ALL CONTAINERS!!!"
    docker-compose -f docker-compose.prod.yml down -v --remove-orphans
    docker-compose -f docker-compose.dev.yml down -v --remove-orphans
fi
