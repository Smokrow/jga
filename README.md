# HOW TO SETUP
## Python 3 Backend for Sound
Install all the dependencies. 
Setup a systemd service on startup to run main.py. This will start the server once it is booted up

## VueJS Frontend
Install Nginx server. Setup the main page to link to the static build. Proxy every call to the /api url to the Flask server running with systemd.

## Misc stuff
Install Chromium and setup the Kioskmode for it.
/home/pi/.config/lxsession/LXDE_pi/autostart
here you can setup a auto start of Chromium and deactivate the mouse clutter
