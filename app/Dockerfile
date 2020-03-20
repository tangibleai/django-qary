# pull official base image
FROM python:3.7.0-alpine

# create directory for the app user
RUN mkdir -p /home/app/midata

# set work directory
WORKDIR /usr/src/app

# prevent python interpreter from writing of .pyc files and buffering of stdout/err
# equivalent to: `python -B -u`
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy django project from host (including requirements.txt) into container
COPY . /usr/src/app/

RUN apk update && apk add postgresql-dev gcc cmake ccache abuild binutils python3-dev musl-dev build-base

RUN pip install --upgrade pip

RUN pip install cython && pip install cymem

RUN pip install -r requirements.txt

# RUN pip install --upgrade pip \
#  && apk add --no-cache --virtual .build-deps gcc postgresql-dev gcc python3-dev musl-dev build-base \
#  && pip install cython \
#  && pip install -r requirements.txt \
#  && apk del .build-deps

# wait for postgres to boot before migrating db with Django's manage.py migrate
ENTRYPOINT ["/usr/src/app/migrate_db.sh"]
