# docker shared volumes config

in `docker-compose.prod.yml` file

```yaml
  web:
    build:
      context: ./app
      dockerfile: Dockerfile.prod
    command: ['gunicorn', 'main_app.wsgi:application', '-t', '240', '-b', '0.0.0.0:8000']
    volumes:
      - "$HOME/midata/private/static_volume:/home/app/web/staticfiles"
      - "$HOME/midata/private/media_volume:/home/app/web/mediafiles"
```

one qary-docker droplet web container:

```bash
CONTAINERID=$(docker ps | grep -E '.*django-qary_web' | cut -c -12) && docker exec -it $CONTAINERID /bin/bash
python -c 'import os; import pwd; print(pwd.getpwuid(os.getuid()).pw_name)'
app
```

app user is uid 101

or in wsgy.py:


# Problem

when you visit http://qary.ai/upload/ you get 500 error and permission denied in the logs:

```bash
nginx_1  | 91.207.175.126 - - [23/Apr/2020:21:34:25 +0000] "POST /upload/ HTTP/1.1" 500 27 "http://qary.ai/upload/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0" "-"
nginx_1  | 91.207.175.126 - - [23/Apr/2020:21:36:08 +0000] "POST /upload/ HTTP/1.1" 500 27 "http://qary.ai/upload/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0" "-"
web_1    | image_upload: <WSGIRequest: POST '/upload/'>
web_1    | image_file: {image_file}
web_1    | vars(image_file): {image_file}
web_1    | Internal Server Error: /upload/
web_1    | Traceback (most recent call last):
web_1    |   File "/home/app/.local/lib/python3.7/site-packages/django/core/handlers/exception.py", line 34, in inner
web_1    |     response = get_response(request)
web_1    |   File "/home/app/.local/lib/python3.7/site-packages/django/core/handlers/base.py", line 115, in _get_response
web_1    |     response = self.process_exception_by_middleware(e, request)
web_1    |   File "/home/app/.local/lib/python3.7/site-packages/django/core/handlers/base.py", line 113, in _get_response
web_1    |     response = wrapped_callback(request, *callback_args, **callback_kwargs)
web_1    |   File "/home/app/web/upload/views.py", line 16, in image_upload
web_1    |     filename = fs.save(image_file.name, image_file)
web_1    |   File "/home/app/.local/lib/python3.7/site-packages/django/core/files/storage.py", line 52, in save
web_1    |     return self._save(name, content)
web_1    |   File "/home/app/.local/lib/python3.7/site-packages/django/core/files/storage.py", line 266, in _save
web_1    |     fd = os.open(full_path, self.OS_OPEN_FLAGS, 0o666)
web_1    | PermissionError: [Errno 13] Permission denied: '/home/app/web/mediafiles/qary_question_repo.md'
```

# Sledgehammer security

inside `scripts/build.sh`:

```bash

# docker-compose ...

chmod -R a-w ~/midata/private/static_volume/
```
