# crawlers trying to retreive wordpress config

# Problem


```bash
root@docker-s-1vcpu-1gb-sfo2-01:~/django-qary# docker-compose -f docker-compose.prod.yml logs -f
Attaching to django-qary_nginx_1, django-qary_web_1, django-qary_db_1, es, rd01
nginx_1  | 2020/04/23 15:19:27 [error] 7#7: *1 connect() failed (111: Connection refused) while connecting to upstream, client: 94.73.23.73, server: , request: "GET / HTTP/1.1", upstream: "http://192.168.144.4:8000/", host: "159.89.143.171:80"
nginx_1  | 94.73.23.73 - - [23/Apr/2020:15:19:27 +0000] "GET / HTTP/1.1" 502 559 "-" "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36" "-"
nginx_1  | 2020/04/23 15:19:27 [error] 7#7: *4 connect() failed (111: Connection refused) while connecting to upstream, client: 94.73.23.73, server: , request: "GET / HTTP/1.1", upstream: "http://192.168.144.4:8000/", host: "159.89.143.171:80"
nginx_1  | 94.73.23.73 - - [23/Apr/2020:15:19:27 +0000] "GET / HTTP/1.1" 502 157 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7" "-"
nginx_1  | 2020/04/23 15:19:27 [error] 7#7: *3 connect() failed (111: Connection refused) while connecting to upstream, client: 94.73.23.73, server: , request: "GET / HTTP/1.1", upstream: "http://192.168.144.4:8000/", host: "159.89.143.171:80"
nginx_1  | 94.73.23.73 - - [23/Apr/2020:15:19:27 +0000] "GET / HTTP/1.1" 502 559 "-" "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36" "-"
nginx_1  | 94.73.23.73 - - [23/Apr/2020:15:19:27 +0000] "GET / HTTP/1.1" 502 559 "-" "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36" "-"
nginx_1  | 2020/04/23 15:19:27 [error] 7#7: *7 connect() failed (111: Connection refused) while connecting to upstream, client: 94.73.23.73, server: , request: "GET / HTTP/1.1", upstream: "http://192.168.144.4:8000/", host: "159.89.143.171:80"
nginx_1  | 94.73.23.73 - - [23/Apr/2020:15:19:27 +0000] "GET / HTTP/1.1" 502 559 "-" "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36" "-"
nginx_1  | 2020/04/23 15:19:27 [error] 7#7: *8 connect() failed (111: Connection refused) while connecting to upstream, client: 94.73.23.73, server: , request: "GET / HTTP/1.1", upstream: "http://192.168.144.4:8000/", host: "159.89.143.171:80"
nginx_1  | 2020/04/23 15:19:28 [error] 7#7: *11 connect() failed (111: Connection refused) while connecting to upstream, client: 94.73.23.73, server: , request: "GET / HTTP/1.1", upstream: "http://192.168.144.4:8000/", host: "159.89.143.171:80"
nginx_1  | 94.73.23.73 - - [23/Apr/2020:15:19:28 +0000] "GET / HTTP/1.1" 502 559 "-" "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36" "-"
nginx_1  | 2020/04/23 15:41:12 [error] 7#7: *13 connect() failed (111: Connection refused) while connecting to upstream, client: 62.210.172.66, server: , request: "GET /wp-admin/admin-ajax.php?action=duplicator_download&file=../wp-config.php HTTP/1.1", upstream: "http://192.168.144.4:8000/wp-admin/admin-ajax.php?action=duplicator_download&file=../wp-config.php", host: "storydecoder.com"
nginx_1  | 62.210.172.66 - - [23/Apr/2020:15:41:12 +0000] "GET /wp-admin/admin-ajax.php?action=duplicator_download&file=../wp-config.php HTTP/1.1" 502 559 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36" "-"
web_1    | Waiting for postgres...
web_1    | chown: invalid user: ‘postgres’
web_1    | db: forward host lookup failed: Unknown host
web_1    | db: forward host lookup failed: Unknown host
web_1    | db: forward host lookup failed: Unknown host
web_1    | db: forward host lookup failed: Unknown host
web_1    | db: forward host lookup failed: Unknown host
web_1    | db: forward host lookup failed: Unknown host
web_1    | db: forward host lookup failed: Unknown host
```
