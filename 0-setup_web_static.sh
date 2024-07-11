#!/usr/bin/env bash
# Preparing my webservers for deployment of web_static.


# update, upgrade, install nginx
sudo apt-get -y update && sudo apt-get -y upgrade

sudo apt-get -y install nginx


# Creating files and folders
# p option is for creating parent directories if necessary, if parent exists, no error raised
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# craete simple html file for testing purposes
echo "Tesstiiiing Nginx Configuration" >> /data/web_static/releases/test/index.html

# Create symbolic link that should be deleted every time script is run, hence "f"
ln -fs /data/web_static/releases/test/ /data/web_static/current

# /data folder's ownership to user and group("R" for recursive)
chown -R ubuntu:ubuntu /data

# Update the Nginx configuration to serve the content of
# /data/web_static/current/ to hbnb_static
# We use the alias directive to configure nginx to serve content from a specific directory.
# For ex when accessing:https://mydomainname.tech/hbnb_static,
# Nginx will serve content from this: /data/web_static/current/

sed -i "/listen 80 default_server;/a location /hbnb_static {alias /data/web_static/current/;}" /etc/nginx/sites-available/default

sudo ufw allow "Nginx HTTP"

sudo nginx -t

sudo service nginx restart
exit 0
