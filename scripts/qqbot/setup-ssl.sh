#!/usr/bin/env bash
# -*- coding: utf-8 -*-

sudo apt update
sudo apt install python3 python3-venv libaugeas0 -y 
sudo apt-get remove certbot
sudo python3 -m venv /opt/certbot/
sudo /opt/certbot/bin/pip install --upgrade pip
sudo /opt/certbot/bin/pip install certbot certbot-nginx

if [ -f /usr/bin/certbot ]; then 
	rm -f /usr/bin/certbot
fi
sudo ln -s /opt/certbot/bin/certbot /usr/bin/certbot

sudo certbot --nginx


# add crontab task to automatic renew ssl certificate
crontab_task="0 0,12 * * * root /opt/certbot/bin/python -c 'import random; import time; time.sleep(random.random() * 3600)' && sudo certbot renew -q"
ret=$(cat /etc/crontab | grep -xF "$crontab_task")
if [ -z "$ret" ]; then
	echo "$crontab_task" | sudo tee -a /etc/crontab > /dev/null
fi

# Upgrade Certbot Monthly
sudo /opt/certbot/bin/pip install --upgrade certbot certbot-nginx