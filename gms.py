import yaml
import sys
import RPi.GPIO as GPIO
import time
import adafruit_dht
import board
#import Adafruit_DHT

with open("config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

class GMS:
    def __init__(self):
        #GPIO Mode BCM - GPIO numbering
        dht_pin = cfg["Temp&Hum"]["SIG"]
        self.dht= adafruit_dht.DHT11(getattr(board, dht_pin))
    def get_temp_hum(self):
        #humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, self.dht)
        temperature = self.dht.temperature
        humidity = self.dht.humidity
        return humidity, temperature

if __name__ == "__main__":
    print(cfg)
    gms1 = GMS()
    print(gms1.get_temp_hum())
