# PAA LEDs
Software to controll LEDs for workcells on a Raspberry Pi.

This software is written in Python. The intention is that the Pi will run various pre-installed light animations, which can be updated as necessary.

## Packages to Install

Before beginning, the following packages need be installed:
* rpi_ws281x
* adafruit-circuitpython-neopixel

These can be installed from the from the commandline using the code below:

`sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel`

## Watchdog file

To get this code to run at startup, there is a watchdog program written that is to be run every minute by the crontab.

Add the line below to the crontab to run the watchdog program every minute:

`* * * * * [command to be run] &`

The ampasand at the end ensures the program is run silently.

It is also necessary to change the permissions on both the watchdog program and the the program to be called, using:

`chmod 755 [path to script]`
