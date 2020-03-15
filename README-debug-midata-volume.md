This is the sequence that worked.

```bash
docker volume prune
docker volume rm django-qary_midata
docker volume ls
sudo service docker stop
sudo service docker start
./build.sh prod
```

Initial trial and error that got nowhere, though it did work a couple times unpredictably.


```bash
10413  ls hello_django/
10414  ls /tmp/midata
10415  ls /tmp/midata/public
10416  ls /home/app
10417  ls /code
10418  cd /code
10419  ls 
10420  cd ..
10421  more docker-compose.prod.yml 
10422  nano nano nginx/nginx.conf 
10423  more docker-compose.prod.yml 
10424  rm /tmp/midata
10425  ./build.sh 
10426  ./build.sh prod
10427  ls /tmp
10428  ls /tmp/midata
10429  git log --stat
10430  git log --stat | grep -A6 -B3 'tmp/midata'
10431  git log --stat | grep -A6 -B5 'tmp/midata'
10432  git checkout b04823 -b develop
10433  ./build.sh prod
10434  ufw tcp:1337 allow
10435  lsof -i :1337
10436  lsof -i :13
10437  docker ps -a
10438  more ufw status
10439  ls -al
10440  ls app/
10441  cd app
10442  cd hello_django/
10443  ls -al
10444  cd ..
10445  ls -al
10446  cd ..
10447  find . -name midata
10448  more docker-compose.prod.yml 
10449  ls /tmp
10450  mkdir /tmp/midata
10451  ls -al
10452  cd app
10453  ls -al
10454  cd staticfiles/
10455  ls -al
10456  ls -al
10457  cd ..
10458  cd ..
10459  more build.sh
10460  docker-compose down -v --remove-orphans
10461  docker-compose -f docker-compose.prod.yml up -d
10462  touch /tmp/midata/readme
10463  exit
10464  workon django-qary
10465  git branch
10466  git push -u origin develop
10467  git status
10468  more .build.sh.swp
10469  exit
10470  nano build.sh
10471  git diff
10472  nano nginx/nginx.conf 
10473  more nginx/nginx.conf 
10474  cd nginx/
10475  ls -al
10476  more nginx.conf
10477  git diff
10478  git status
10479  ls -al
10480  exit
10481  git pull
10482  workon django-qary
10483  git pull
10484  git checkout develop
10485  git diff
10486  git checkout master
10487  git log
10488  git commit -am 'updated build.sh for dev prod stop'
10489  git push
10490  nano docker-compose.yml 
10491  nano docker-compose.prod.yml 
10492  ./build.sh prod
10493  touch /tmp/midata/readme
10494  ls -al /tmp
10495  rm -r /tmp/midata
10496  ./build.sh prod
10497  ls -al /tmp
10498  nano nginx/nginx.conf 
10499  nano docker-compose.yml 
10500  nano docker-compose.prod.yml 
10501  ls /home/hobs/midata
10502  ./build.sh prod
10503  nano docker-compose.prod.yml 
10504  ./build.sh prod
10505  nano docker-compose.prod.yml 
10506  docker volume rm -f midata
10507  docker volume rm -f midata
10508  nano docker-compose.prod.yml 
10509  ./build.sh prod
10510  ls -al /midata
10511  ls -adl /midata
10512  sudo service docker restart
10513  ./build.sh prod
10514  more docker-compose.prod.yml 
10515  ls /midata
10516  ls /midata/dockered
10517  touch /midata/dockered/readme
10518  sudo touch /midata/dockered/readme
10519  ls -ald /midata/
10520  ls -ald /midata/dockered/
10521  sudo ln -s /midata/public/chatbot /midata/dockered/chatbot
10522  sudo chown root:root /midata/dockered/chatbot
10523  sudo chmod +xrw /midata/dockered/chatbot
10524  ls -al /midata/dockered/chatbot
10525  ls /midata/dockered/chatbot
10526  sudo ln /midata/public/us-zip-code-latitude-and-longitude.csv /midata/dockered/
10527  ls -al /midata/dockered/chatbot/
10528  sudo service nginx up
10529  ./build.sh stop
10530  sudo service nginx start
10531  ls -hal /midata/dockered/
10532  ./build.sh prod
10533  docker ps -a
10534  docker ps
10535  nano /etc/nginx/sites-enabled/django-totalgood.org.conf 
10536  sudo nano /etc/nginx/sites-enabled/django-totalgood.org.conf 
10537  ls /midata
10538  ls /midata/dockered/
10539  ls -al /midata/dockered/
10540  sudo chmod 755 /midata/dockered/chatbot
10541  sudo chmod 755 /midata/dockered/
10542  sudo service nginx reload
10543  sudo nano /etc/nginx/sites-enabled/django-totalgood.org.conf 
10544  sudo service nginx reload
10545  sudo service nginx start
10546  sudo service nginx status
10547  sudo nano /etc/nginx/sites-enabled/django-totalgood.org.conf 
10548  sudo service nginx start
10549  sudo nano /etc/nginx/sites-enabled/django-totalgood.org.conf 
10550  sudo nano /etc/nginx/nginx.conf
10551  cp /etc/nginx/nginx.conf nginx/nginx.host.conf 
10552  exit
10553  exit
10554  tmux
10555  exit
10556  workon django-qary
10557  nano nginx/nginx.conf
10558  ./build prod
10559  ./build.sh prod
10560  docker ps
10561  man cp
10562  rm -r /midata/dockered/chatbot/
10563  rm /midata/dockered/chatbot/
10564  ls -al /midata/dockered/chatbot/
10565  ls -ald /midata/dockered/chatbot/
10566  ls -ald /midata/dockered/
10567  ls -al /midata/dockered/
10568  rm /midata/dockered
10569  sudo rm /midata/dockered
10570  sudo rm -f /midata/dockered
10571  ls -hal /midata/
10572  chown hobs:hobs /midata/dockered
10573  sudo chown hobs:hobs /midata/dockered
10574  sudo chown hobs:hobs /midata/dockered/chatbot
10575  ls -al /midata/dockered
10576  sudo chown hobs:hobs /midata/dockered/chatbot/
10577  ls -al /midata/dockered
10578  rm /midata/dockered/chatbot
10579  cd /midata/dockered/
10580  ls -hal
10581  cd /midata/
10582  ls -al
10583  sudo chown root:root dockered/
10584  sudo chmod -R 755 root:root dockered/
10585  sudo chown -R root:root dockered/
10586  sudo chmod -R 755 dockered/
10587  cd dockered/
10588  ls -al
10589  cd ..
10590  ls -hal /midata/links-to-public/
10591  ls -hal /midata/links-to-public/chatbot/
10592  df
10593  df -hal
10594  df -h
10595  df -h
10596  df -h
10597  df -h
10598  workon django-qary
10599  nano docker-compose.prod.yml 
10600  cd /midata
10601  ./build.sh prod
10602  cd links-to-public/
10603  du -h
10604  df -h
10605  cp -al public links-to-public
10606  df -h
10607  ls -hald midata/public
10608  ls -hald /midata/public
10609  ls -hald /midata/links-to-public
10610  nano docker-compose.prod.yml 
10611  ./build.sh prod
10612  docker ps
10613  docker logs web
10614  docker logs nginx
10615  docker logs django-qary_web
10616  docker logs 2f53
10617  docker logs 6b69
10618  more app/hello_django/settings.py 
10619  more .env.prod 
10620  more app/hello_django/settings.py 
10621  nano app/hello_django/settings.py 
10622  ./build.sh prod
10623  more app/hello_django/settings.py 
10624  grep ALLOWED_HOSTS app/hello_django/settings.py 
10625  nano app/hello_django/settings.py 
10626  git status
10627  git commit -am 'allowed hosts fixed'
10628  git push
10629  git branch
10630  exit
10631  ./build.sh prod
10632  ./build.sh prod
10633  ps
10634  docker ps
10635  git pull
10636  git pull
10637  workon django-qary
10638  git pull
10639  exit
10640  ./build.sh prod
10641  sudo service nginx stop
10642  ./build.sh prod
10643  more /etc/nginx/nginx.conf
10644  more /etc/nginx/sites-enabled/django-totalgood.org.conf 
10645  git commit -am "prod won't work unless you already have some dummy certs in /etc/letsencrypt/.../live/totalgood.org/*.pem"
10646  git pull
10647  git pull
10648  git branch
10649  git pull
10650  ./build.sh prod
10651  sudo apt install fahclient
10652  sudo apt search fahclient
10653  sudo apt-get search fahclient
10654  wget https://download.foldingathome.org/releases/public/release/fahclient/debian-stable-64bit/v7.5/fahclient_7.5.1_amd64.deb
10655  mv fahclient_7.5.1_amd64.deb ~/Downloads/
10656  cd ~/Downloads/
10657  ls -al
10658  sudo dpkg -i --force-depends fahclient_7.4.4_amd64.deb
10659  ls
10660  sudo dpkg -i --force-depends fahclient_7.5.1_amd64.deb
10661  sudo service nginx disable
10662  sudo update-rc.d -f nginx disable
10663  sudo update-rc.d -f postgresql disable
10664  sudo service elasticsearch start
10665  who
10666  htop
10667  wget https://download.foldingathome.org/releases/public/release/fahcontrol/debian-stable-64bit/v7.5/fahcontrol_7.5.1_amd64.deb
10668  wget https://download.foldingathome.org/releases/public/release/fahcontrol/debian-stable-64bit/v7.5/fahcontrol_7.5.1-1_all.deb
10669  sudo dpkg -i --force-depends fahcontrol_7.5.1-1_all.deb
10670  fahcontrol
10671  sudo service fahcontrol status
10672  htop
10673  sudo shutdown -r now
10674  htop
10675  workon django-qary
10676  ./build.sh prod
10677  git status
10678  git log --stat
10679  git checkout 3b172 -b feature-nossl
10680  ./build.sh prod
10681  ls /midata/
10682  nano docker-compose.prod.yml 
10683  ./build.sh prod
10684  ls -hal /midata
10685* 
10686  sudo chmod 755 /midata/links-to-public
10687  sudo chmod 755 /midata
10688  ./build.sh stop
10689  ps a
10690  docker ps -a
10691  docker ps
10692* 
10693  nano docker-compose.prod.yml 
10694  ./build.sh stop
10695  ./build.sh prod
10696  ./build.sh stop
10697  nano docker-compose.prod.yml 
10698  rm -r /midata/dockered
10699  rm -r /midata/dockered
10700  sudo rm -r /midata/dockered
10701  ./build.sh prod
10702  ls /midata
10703  sudo chown root:root /midata
10704  sudo chmod 755 /midata
10705  ./build.sh prod
10706  ./build.sh stop
10707  sudo chmod 755 /midata/dockered
10708  sudo mkdir /midata/dockered
10709  sudo chmod 755 /midata/dockered
10710  ./build.sh stop
10711  docker volumes
10712  docker --help
10713  docker volume
10714  docker volume ls
10715  docker volume prume
10716  docker volume prune
10717  docker volume ls
10718  ./build.sh prod
10719  nano nginx/nginx.conf 
10720  docker volume ls
10721  docker volume
10722  docker volume inspect django-qary_midata
10723  docker volume rm django-qary_midata
10724  docker volume inspect django-qary_midata
10725  ./build.sh prod
10726  sudo service docker stop
10727  sudo service docker start
10728  ./build.sh prod
10729  docker ps
```
