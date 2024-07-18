# cpy-jwst-schedule
What is JWST doing, right now? This CircuitPython project will tell you

## Usage

Install Circuitpython 9.1 or newer on an Adafruit Magtag. Setup the wifi workflow by setting up the SSID and password of network, as well as a password for the board.

Run circup to install the libraries:
```
circup --host IP-of-board --password JwstRocks install adafruit_magtag
circup --host IP-of-board --password JwstRocks install adafruit_ntp
```

Add the code from this repo to ``code.py`` .
