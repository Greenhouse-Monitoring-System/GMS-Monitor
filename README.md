# GMS-Monitor

> [!NOTE]  
> Work In Progress

> [!CAUTION]
> This project will be using the Python Virtual Environment located under `gmsenv` folder
> To activate the environment, run the following cmd `source gmsenv/bin/activate` 

## Pi Zero GPIO
```commandline
Description        : Raspberry Pi Zero2W rev 1.0
Revision           : 902120
SoC                : BCM2837
RAM                : 512MB
Storage            : MicroSD
USB ports          : 1 (of which 0 USB3)
Ethernet ports     : 0 (0Mbps max. speed)
Wi-fi              : True
Bluetooth          : True
Camera ports (CSI) : 1
Display ports (DSI): 0

,--oooooooooooooooooooo---.
|  1ooooooooooooooooooo J8|
---+     +---+  PiZero2W  c|
 sd|     |SoC|   Wi V1.0  s|
---+     +---+   Fi       i|
| hdmi            usb pwr |
`-|  |------------| |-| |-'


J8:
   3V3  (1) (2)  5V
 GPIO2  (3) (4)  5V
 GPIO3  (5) (6)  GND
 GPIO4  (7) (8)  GPIO14
   GND  (9) (10) GPIO15
GPIO17 (11) (12) GPIO18
GPIO27 (13) (14) GND
GPIO22 (15) (16) GPIO23
   3V3 (17) (18) GPIO24
GPIO10 (19) (20) GND
 GPIO9 (21) (22) GPIO25
GPIO11 (23) (24) GPIO8
   GND (25) (26) GPIO7
 GPIO0 (27) (28) GPIO1
 GPIO5 (29) (30) GND
 GPIO6 (31) (32) GPIO12
GPIO13 (33) (34) GND
GPIO19 (35) (36) GPIO16
GPIO26 (37) (38) GPIO20
   GND (39) (40) GPIO21
```

## Project Folder Tree

### DHT11 Library Install:
```
pip install adafruit-circuitpython-dht

```
<!--
```
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
sudo apt-get install python3-setuptools
sudo apt-get install python3-dev
cd Adafruit_Python_DHT
sudo python setup.py install --force-pi
sudo apt-get install libgpiod2
```
-->

### PiCamera
```
sudo apt install -y python3-libcamera python3-kms++ libcap-dev
sudo apt install -y python3-prctl libatlas-base-dev ffmpeg

pip install numpy --upgrade

pip install picamera2
```
