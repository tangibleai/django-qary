# Django-qary

Web application, API, and Admin dashboard for the QAry cognitive search engine

## Docker Containers

- web: Django, Django REST Framework, nboost
- nginx: Nginx web server for staticfiles, mediafiles, and /midata
- postgresql: Database for user credentials, profiles
- elastic: ElasticSearch document database

## Install

If you cloned the repo from gitlab you'll want to ignore your changes to .env.* files:

```bash
git update-index --skip-worktree -- .env.*
```

Then you can edit .env.dev and .env.prod to reflect your network settings and credentials without your secrects being tracked by git.


## Building Docker Images

SEE: [testdriven.io](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)

### Development Environment (typically a Mac laptop with Docker Desktop)

To build and run the dev environment:

```bash
$ docker-compose down -v
$ docker-compose -f docker-compose.dev.yml up -d --build
```

Or:

```bash
$ ./scripts/build.sh dev
```

<<<<<<< HEAD

=======
### Production Environment (typically Linux Docker server)
>>>>>>> unstable

To build and run the production containers:

```bash
$ docker-compose down -v

$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
$ docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```

Or:

```bash
$ ./scripts/build.sh prod
```

### Scalable Production Environment

For an actual production deployment with improved security, you'll probably want to use:

    - A fully managed database service (such as RDS)
    - Non-root user for the db and nginx services

For other production tips, see [this Reddit comment](https://www.reddit.com/r/django/comments/bjgod8/dockerizing_django_with_postgres_gunicorn_and/).

You can find the original testdrivenio version of the code in [their github repo](https://github.com/testdrivenio/django-on-docker) repo.
