import yaml
import sys
import RPi.GPIO as GPIO
import time
import adafruit_dht
import board
from picamera2 import Picamera2
import uuid
#import Adafruit_DHT

with open("config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

class GMS:
    def __init__(self):
        #GPIO Mode BCM - GPIO numbering
        dht_pin = cfg["Temp&Hum"]["SIG"]
        self.dht= adafruit_dht.DHT11(getattr(board, dht_pin))
        
        self.picam2 = Picamera2()
        #capture_config = picam2.create_still_configuration()
        #self.picam2 = self.picam2.configure(capture_config)

    def get_temp_hum(self):
        #humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, self.dht)
        temperature = self.dht.temperature
        humidity = self.dht.humidity
        return humidity, temperature

    def get_camera(self):
        self.picam2.start()
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        uid = uuid.uuid4()
        self.picam2.capture_file(f"timelapse/{timestamp}-{uid}.jpg")

if __name__ == "__main__":
    print(cfg)
    gms1 = GMS()
    print(gms1.get_temp_hum())
    gms1.get_camera()
