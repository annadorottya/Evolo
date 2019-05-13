# Evolo

Evolo is a our project for the class 'ICT Innovation' at the University of Trento, Italy. It is device to protect homes from unauthorized drones. It can detect and take over drones (currently only Parrot AR drones are supported).

# Good to know

Start ftp daemon on Raspberry: `python -m pyftpdlib -w`
Always run evolo as root! (Otherwise it can not connect to wifi networks). Or setuid should be used.


# Install

The product itself was designed to be plug-and-play, so there will be no installation needed by the end-user. However for testing here is how to make our code work:

## Get a Raspberry Pi and install Raspbian on the SD card

More onformation on this can be found on the official website of Raspberry Pi: https://www.raspberrypi.org/documentation/installation/installing-images/

## Configure your pi
Boot your freshly installed Raspbian, then run the following commands to expand the filesystem, change root password, optionally change locale.
```
sudo raspi-config
sudo reboot
```

## Update everything
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
sudo reboot
```

## Install the necessary packages
Install a webserver with php for hosting the configuration website, install scapy for sending raw packets and python wifi library for scanning and connecting to wifi.
```
sudo apt-get install apache2 -y
sudo apt-get install php5 libapache2-mod-php5 -y
sudo apt-get install tcpdump graphviz imagemagick python-gnuplot python-crypto python-pyx
sudo apt-get install python-pip
sudo pip install wifi
sudo reboot
```
## Install Evolo
Clone the git repository to the home folder
```
cd /home/pi/
git clone https://github.com/annadorottya/Evolo.git
```
## Make the website accessible
Since the website is in `/home/pi/Evolo/web` we need to link it from `/etc/www/`
```
sudo rm -R /etc/www/html
sudo ln -s /home/pi/Evolo/web /etc/www/html
```
## Change ownership and permissions
First assign the ownership of the website folder to `www-data`. Then assign `listDrones.py` to `root` and set the userid and groupid on it. It will run this file in the name of root and not the name of the caller. This is to make it possible to list the nearby drones on the webinterface, since the webserver runs in the name of `www-data` which is a non-root user, but only root has the rights to list the wifi networks. 

```
sudo chown www-data:www-data -R /home/pi/Evolo/web
sudo chown root:root /home/pi/Evolo/code/listDrones.py
sudo chmod 6775 /home/pi/Evolo/code/listDrones.py

```
## Make Evolo autostart at boot
Since Evolo need to run everytime the Raspberry Pi boots up, let's add it to crontab. First run the following command:
```
crontab -e
```
Then add this line to the end of the file:
```
@reboot sudo python /home/pi/Evolo/code/main.py
```
Save and exit the text editor (in case of nano press `Ctrl+X` then `y` and `Enter`) and reboot your Raspberry Pi:
```
sudo reboot
```

# Install the code on the Arduino
The Raspberry Pi is now ready. Let's install the code on the Arduino. Connect the Arduino to your computer, and install the Arduino software from https://www.arduino.cc/. Now clone our repository from Github to your computer:
```
git clone https://github.com/annadorottya/Evolo.git
```
Open `arduinoWithScreen` project in the Arduino IDE and upload it to your Arduino. Connect your Arduino to the Raspberry Pi and the installation is done, Evolo is ready for operation.
