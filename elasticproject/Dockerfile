FROM python:latest

# create directory for the app user
# RUN mkdir -p /home/app/midata
RUN mkdir -p /usr/src/elasticproject

# set work directory
WORKDIR /usr/src/elasticproject

# prevent python interpreter from writing of .pyc files and buffering of stdout/err
# equivalent to: `python -B -u`
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN apt-get update 
COPY ./requirements.txt /usr/src/elasticproject/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt \
    && pip3 install djangorestframework

COPY . /usr/src/elasticproject/