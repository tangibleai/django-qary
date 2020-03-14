###########################################################################################
# Development server container Dockerfile
#
FROM python:3.7.0-alpine

# create directory for the app user
RUN mkdir -p /home/app/midata

# set work directory
WORKDIR /usr/src/app

# prevent python interpreter from writing of .pyc files and buffering of stdout/err
# equivalent to: `python -B -u`
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# copy django project from host (including requirements.txt) into container
COPY . /usr/src/app/

RUN pip install --upgrade pip && pip install -r requirements.txt

# wait for postgres to boot before migrating db with Django's manage.py migrate
ENTRYPOINT ["/usr/src/app/migrate_db.sh"]
