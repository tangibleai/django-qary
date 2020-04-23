# docker shared volumes config

in `docker-compose.prod.yml` file

```yaml
  web:
    build:
      context: ./app
      dockerfile: Dockerfile.prod
    ...
```

in app/Dockerfile.prod

```yaml

```

# Problem


```bash
$ docker-compose -f docker-compose.prod.yml logs -f
es ...
db_1 ...
rd01 ...
nginx_1 ...
web_1    | Bad Request: //www/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php
web_1    | Attempting to connect to 'es:9200'...
web_1    | Attempting to search for text='Barack obama'
web_1    |  in index='wikipedia' using client=<Elasticsearch([{'host': 'es', 'port': 9200}])>
web_1    |
web_1    | POST http://es:9200/wikipedia/_search [status:200 request:0.302s]
web_1    | Attempting to connect to 'es:9200'...
web_1    | Attempting to search for text=''
web_1    |  in index='wikipedia' using client=<Elasticsearch([{'host': 'es', 'port': 9200}])>
web_1    |
web_1    | POST http://es:9200/wikipedia/_search [status:200 request:0.047s]
web_1    | Internal Server Error: /qa/
web_1    | Traceback (most recent call last):
web_1    |   File "/home/app/.local/lib/python3.7/site-packages/django/core/handlers/exception.py", line 34, in inner
web_1    |     response = get_response(request)
web_1    |   File "/home/app/.local/lib/python3.7/site-packages/django/core/handlers/base.py", line 115, in _get_response
web_1    |     response = self.process_exception_by_middleware(e, request)
web_1    |   File "/home/app/.local/lib/python3.7/site-packages/django/core/handlers/base.py", line 113, in _get_response
web_1    |     response = wrapped_callback(request, *callback_args, **callback_kwargs)
web_1    |   File "/home/app/web/elastic_app/views.py", line 50, in answers_index
web_1    |     results = find_answers(question)
web_1    |   File "/home/app/web/elastic_app/es_search.py", line 93, in find_answers
web_1    |     bot_reply = QABOT.reply(statement, context=snippet)
web_1    | TypeError: reply() got an unexpected keyword argument 'context'
```

and later on...

```bash
rd01     | 1:M 23 Apr 2020 17:55:37.174 * Ready to accept connections
web_1    | Attempting to search for text=''
web_1    |  in index='wikipedia' using client=<Elasticsearch([{'host': 'es', 'port': 9200}])>
web_1    |
web_1    | POST http://es:9200/wikipedia/_search [status:200 request:0.038s]
web_1    | image_upload: <WSGIRequest: GET '/upload/'>
nginx_1  | 91.207.175.126 - - [23/Apr/2020:18:28:37 +0000] "GET /upload/ HTTP/1.1" 200 300 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0" "-"
web_1    | Attempting to connect to 'es:9200'...
web_1    | Attempting to search for text=''
web_1    |  in index='wikipedia' using client=<Elasticsearch([{'host': 'es', 'port': 9200}])>
web_1    |
web_1    | POST http://es:9200/wikipedia/_search [status:200 request:0.095s]
nginx_1  | 70.95.128.14 - - [23/Apr/2020:18:37:05 +0000] "GET / HTTP/1.1" 200 6902 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0" "-"
web_1    | Not Found: /favicon.ico
nginx_1  | 70.95.128.14 - - [23/Apr/2020:18:37:05 +0000] "GET /favicon.ico HTTP/1.1" 404 77 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0" "-"
```

# Sledgehammer security

```bash
chmod -R a+w ~/midata/private/static_volume/

# docker-compose ...

chmod -R a-w ~/midata/private/static_volume/
```
