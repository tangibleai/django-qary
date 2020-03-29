###########################################################################################
# Development server container Dockerfile
#
FROM python:3.7-buster

# create directory for the app user
RUN mkdir -p /home/app/midata

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# prevent python interpreter from writing of .pyc files and buffering of stdout/err
# equivalent to: `python -B -u`
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app/

# COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install cython && pip install cymem

#  && pip install tensorflow-cpu==2.1

RUN pip install -r requirements.txt


EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
