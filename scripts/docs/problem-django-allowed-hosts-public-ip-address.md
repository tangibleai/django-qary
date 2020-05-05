problem-django-allowed-hosts-public-ip-address


## Problem

## Solution

Make sure you have the right local IP address:

```bash
export PUBLIC_IP=$(curl -q ifconfig.co)
echo "PUBLIC_IP=$PUBLIC_IP"
echo "PUBLIC_IP=$PUBLIC_IP" >> .env.prod
```

You'll need to then make sure the ALLOWED_HOSTS variable contains that IP address manually. The following code won't work because the DJANGO_ALLOWED_HOSTS variable is not exported in .env.prod . Docker doesn't allow export statements in ENV files.

```bash
echo "DJANGO_ALLOWED_HOSTS='${PUBLIC_IP} ${DJANGO_ALLOWED_HOSTS}'"
echo 'DJANGO_ALLOWED_HOSTS="'"${PUBLIC_IP} "'${DJANGO_ALLOWED_HOSTS}"' >> .env.prod
```

So on the 3rd line in `.env.prod` below you shoudl see that IP address after you've manually copied and pasted it into that list of space-delimitted domains:

```bash
DEBUG=0
SECRET_KEY='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWX'
DJANGO_ALLOWED_HOSTS="localhost 127.0.0.1 [::1] $PUBLIC_IP nlpia.org www.nlpia.org qary.nlpia.org www.qary.ai qary.ai qary.me www.qary.me"

SQL_ENGINE=django.db.backends.postgresql
SQL_HOST=db
SQL_PORT=5432
