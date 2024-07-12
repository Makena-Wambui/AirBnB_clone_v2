#!/usr/bin/env bash
# Preparing my webservers for deployment of web_static.

# Update, upgrade, install nginx
sudo apt-get -y update && sudo apt-get -y upgrade
sudo apt-get -y install nginx

# Creating files and folders
# -p option is for creating parent directories if necessary, if parent exists, no error raised
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create simple html file for testing purposes
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Remove old symbolic link and create a new one
sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# /data folder's ownership to user and group ("-R" for recursive)
sudo chown -R ubuntu:ubuntu /data

# Update the Nginx configuration to serve the content of
# /data/web_static/current/ to hbnb_static
# Use the alias directive to configure nginx to serve content from a specific directory.
# For example, when accessing https://mydomainname.tech/hbnb_static,
# Nginx will serve content from this: /data/web_static/current/
# Backup the original Nginx configuration file
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup

# Ensure the location block is not duplicated
sudo sed -i '/location \/hbnb_static {/d' /etc/nginx/sites-available/default
sudo sed -i "/listen 80 default_server;/a location /hbnb_static { alias /data/web_static/current/; }" /etc/nginx/sites-available/default

# Allow Nginx HTTP through the firewall
sudo ufw allow 'Nginx HTTP'

# Test Nginx configuration
sudo nginx -t

# Restart Nginx service
sudo service nginx restart

exit 0
