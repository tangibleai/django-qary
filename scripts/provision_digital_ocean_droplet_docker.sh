#!/usr/bin/env bash

# user root
mkdir -p /mnt/volume_sfo2_01
mount -o discard,defaults,noatime /dev/disk/by-id/scsi-0DO_Volume_volume-sfo2-01 /mnt/volume_sfo2_01
echo '/dev/disk/by-id/scsi-0DO_Volume_volume-sfo2-01 /mnt/volume_sfo2_01 ext4 defaults,nofail,discard0' | sudo tee -a /etc/fstab
mkdir -p ~/code/chatbot
cd ~/code/chatbot
ssh-keygen -P "" -q -t rsa -f ~/.ssh/id_rsa_gitlab
cat ~/.ssh/id_rsa_gitlab.pub
read -p "Copy the public key above and paste into gitlab settings then hit [ENTER]: " continue_script
git clone git@gitlab.com:tangibleai/django-qary
cd django-qary

# make sure the ~/midata/public directory is available for docker volume mounting
sudo ln -s /mnt/volume_sfo2_01 ~/midata
sudo chown -R root:docker ~/midata
sudo chmod -R g+rwx ~/midata
sudo chmod -R +rwx ~/midata
mkdir -p ~/midata/public/chatbot
mkdir -p ~/midata/public/models
mkdir -p ~/midata/public/talks

# get rid of some large files to conserve disk space on the digital ocean block storage volume
rm -rf ~/midata/public/talks/2016-05-01--CivicU-Machine-Learning/.git
rm -rf ~/midata/public/talks/2016-05-01--CivicU-Machine-Learning/lessons/shared-resources/mnist
cd ~/midata/public/chatbot/nlpia-bot-data/simple-transformers
rm -rf checkpoint-10000
rm -rf checkpoint-14000
rm -rf checkpoint-18000
rm -rf checkpoint-20000
rm -rf checkpoint-24000
rm -rf checkpoint-26000
rm -rf checkpoint-4000
rm -rf checkpoint-6000
rm -rf checkpoint-8000
docker rm $(docker ps -q)
docker rmi $(docker ps -q)
docker system prune

# build and run the docker containers!
cd ~/code/chatbot/django-qary/
./scripts/build.sh prod
