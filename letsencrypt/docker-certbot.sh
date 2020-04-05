#!/usr/bin/env bash
# docker-certbot.sh [prod|dev]

# References:
#   https://www.humankode.com/ssl/how-to-set-up-free-ssl-certificates-from-lets-encrypt-using-docker-and-nginx

if [ "$1" == "dev" ]; then
sudo docker run -it --rm \
	-v /docker-volumes/etc/letsencrypt:/etc/letsencrypt \
 	-v /docker-volumes/var/lib/letsencrypt:/var/lib/letsencrypt \
	-v /docker/letsencrypt-docker-nginx/src/letsencrypt/letsencrypt-site:/data/letsencrypt \
	-v "/docker-volumes/var/log/letsencrypt:/var/log/letsencrypt" \
	certbot/certbot certonly \
		--webroot \
		--register-unsafely-without-email \
		--agree-tos \
		--webroot-path=/data/letsencrypt \
		--staging \
			-d totalgood.org \
			-d www.totalgood.org \
			-d gpu.totalgood.org \
			-d qary.totalgood.org \
			-d es.totalgood.org \
			-d jupyter.totalgood.org \
			-d rpi.totalgood.org

elif [ "$1" == "prod" ]; then
# remove all staging artifacts:
sudo rm -rf /docker-volumes/

# rerun this command after staging works
sudo docker run -it --rm \
        -v /docker-volumes/etc/letsencrypt:/etc/letsencrypt \
        -v /docker-volumes/var/lib/letsencrypt:/var/lib/letsencrypt \
        -v /docker/letsencrypt-docker-nginx/src/letsencrypt/letsencrypt-site:/data/letsencrypt \
        -v "/docker-volumes/var/log/letsencrypt:/var/log/letsencrypt" \
        certbot/certbot certonly \
                --webroot \
                --email=hobson@totalgood.com \
                --agree-tos \
                --webroot-path=/data/letsencrypt \
                        -d totalgood.org \
                        -d www.totalgood.org \
                        -d gpu.totalgood.org \
                        -d qary.totalgood.org \
                        -d es.totalgood.org \
                        -d jupyter.totalgood.org \
                        -d rpi.totalgood.org

else:
  usage: sudo docker-certbot.sh [prod|dev]

  sudo docker-certbot.sh prod: renews or requests real certificates and you're limited to 20 requests a week from an IP address
  sudo docker-certbot.sh dev: does a "--staging" certbot run and does not provide the hobson@totalgood.com e-mail address

fi
