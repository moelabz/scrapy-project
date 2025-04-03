#!/bin/bash
# Install Google Chrome and ChromeDriver

# Install Google Chrome (Render already has this, but in case it's missing)
apt-get update
apt-get install -y google-chrome-stable

# Install ChromeDriver
CHROME_DRIVER_VERSION=`google-chrome --version | sed 's/Google Chrome //'`
CHROME_DRIVER_VERSION=`echo $CHROME_DRIVER_VERSION | sed 's/\..*//g'`
wget https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver

# Clean up
rm chromedriver_linux64.zip
