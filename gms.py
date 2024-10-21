import yaml
import RPi.GPIO as GPIO
import time

with open("config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

class GMS:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.dht = cfg["Temp&Hum"]["SIG"]

if __name__ == "__main__":
    gms1 = GMS()
    print(cfg)