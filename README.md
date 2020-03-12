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

To build and run the dev environment:

```bash
$ docker-compose down -v
$ docker-compose -f docker-compose.yml up -d --build
```



To build and run the production containers:

```bash
$ docker-compose down -v

$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
$ docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```

In terms of actual deployment to a production environment, you'll probably want to use a:

    Fully managed database service (like RDS) rather than managing your own Postgres instance within a container.
    Non-root user for the db and nginx services

For other production tips, review [this discussion](https://www.reddit.com/r/django/comments/bjgod8/dockerizing_django_with_postgres_gunicorn_and/).

You can find the code in the [django-on-docker](https://github.com/testdrivenio/django-on-docker) repo.
