# Musicvoting

&copy; 2015 [Tobias Trumm](mailto:tobiastrumm@uni-muenster.de) licensed under GPLv3

## Info

This project gives your guests the option to vote on the tracks which should be played next on your party. To do so, it runs a local web server and an access point. When your guests connect their mobile devices to the "Musicvoting" wifi, all browser requests will be redirected to the local "musicvoting.lan" site, where they can vote for the tracks which should be played next. 

Currently I am running this project on a Raspberry Pi B. If you want to setup an access point, you will also need a wifi adapter.

## Installation

First I should note that some basic knowledge of Python and web servers will be helpful. This project is currently not optimized for an easy and quick setup.

1. Clone this repository.
2. Install the Python packages pygame, tinytag, django and flup.
3. Open the file `musicvoting/settings.py`. The variable `MUSICVOTING_MUSIC_DIR` should point to the directory where your music is stored. `STATIC_ROOT` points to the directory which will contain all static files for the web server.
5. In the root directory of the project, run `python manage.py migrate` to generate the sqlite database, which is needed by django and where information about the tracks wil be stored.
6. Now run `python manage.py collectstatic` which will put all required static files into the `STATIC_ROOT`directory.
7. We haven't installed a web server yet. I am using lighttpd on my Raspberry Pi. Run `sudo apt-get install lighttpd` to install lighttpd.
8. If you want to setup an access point, you will also need to install hostapd and dnsmasq: `sudo apt-get install hostapd dnsmasq`
9. Run `ifconfig` to get the ip address of your Raspberry Pi.
9. The easiest way to setup lighttpd is to copy the `lighttpd.conf` file from `configfiles` to `/etc/lighttpd/`. Make sure that all settings (like server.document-root and socket) in the config file are correctly pointing to your musicvoting directory. Also make sure that the ip addresses in the lines starting with $HTTP are matching with the ip address of your Raspberry Pi. Then restart lighttpd with `sudo service lighttpd restart`.
10. Now open (edit) the `start.sh` script in the project directory. Make sure that the variable `PROJDIR`points to the project directory.
11. Now execute `start.sh`. You won't hear any music yet, because the player crashed because it couldn't find any tracks in the database. We will fix that in a second.
12. Run `python manage.py createsuperuser` to create an admin account for your site.
13. If everything went well, you should now be able to open `IP_ADDRESS/admin` in a browser on a device that is in the same network as your Raspberry Pi. Log in with the admin account you created in the previous step.
14. Actually you don't need to change anything on the admin site, you just need to be logged in as a superuser for the next step. Navigate to `IP_ADDRESS/dbimport` to import the tracks from your music directory into the database. This might take a while, depending on how many tracks have to be imported. 
15. After the import has finished, run `start.sh` again. After some seconds music should start playing (if some speakers are connected). Now you can navigate to the main page by entering `IP_ADDRESS/` in your browser.
16. Now you can access the musicvoting site from your local network, but the access point isn't configured yet.
17. First assign a static ip address to your wifi connection by editing `/etc/network/interfaces`. Look at `configfiles/interfaces` for an example.
18. Now edit `/etc/hostapd/hoastapd.conf` by changing the option `DAEMON_CONF` to `DAEMON_CONF="/etc/hostapd/hostapd.conf"` and create the ``/etc/hostapd/hostapd.conf` file. You can use the `configfiles/hostapd.conf` file for that.
19. Now open the `etc/dnsmasq.conf` file and change the settings `interface` to `interface=wlan0` (assuming that your wifi adapter belongs to interface wlan0) and `dhcp-range` to `dhcp-range=192.168.2.2,192.168.2.100,255.255.255.0,12h`. Also change `address` to `address=/#/192.168.2.1`. This will redirect every request (like example.com) on your access point to the musicvoting.lan site.
20. If everything went well you should now be able to see and to connect to the musicvoting wifi. 