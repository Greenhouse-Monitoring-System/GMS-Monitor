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
        self.TRIG_PIN = cfg["Sonar"]["TRIG"]
        self.ECHO_PIN = cfg["Sonar"]["ECHO"]
        GPIO.setup(self.TRIG_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)
        self.picam2 = Picamera2()
        #capture_config = picam2.create_still_configuration()
        #self.picam2 = self.picam2.configure(capture_config)
        self.RELAY_IN1 = cfg["Relay"]["IN1"]
        self.RELAY_IN2 = cfg["Relay"]["IN2"]
        GPIO.setup(self.RELAY_IN1, GPIO.OUT)
        GPIO.setup(self.RELAY_IN2, GPIO.OUT)

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

    def get_distance(self):
        GPIO.output(self.TRIG_PIN, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.TRIG_PIN, GPIO.LOW)

        # Measure the duration for the echo pulse
        while GPIO.input(self.ECHO_PIN) == 0:
            pulse_start = time.time()

        while GPIO.input(self.ECHO_PIN) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        # Calculate the distance based on the speed of sound (34300 cm/s)
        distance = pulse_duration * 34300 / 2

        return distance

    def relay_WaterON(self, duration: int):
        GPIO.output(self.RELAY_IN1, GPIO.LOW)
        time.sleep(duration)
        GPIO.output(self.RELAY_IN1, GPIO.HIGH)
        return True

    def relay_FanON(self, duration: int):
        GPIO.output(self.RELAY_IN2, GPIO.LOW)
        time.sleep(duration)
        GPIO.output(self.RELAY_IN2, GPIO.HIGH)
        return True

    def soilMoisture(self):
        #GPIO.input()
        return False

if __name__ == "__main__":
    print(cfg)
    gms1 = GMS()
    print("Temp and Humidity",gms1.get_temp_hum())
    gms1.get_camera()
    print(gms1.get_distance(), "cm")
    print("Relay Test")
    gms1.relay_WaterON(4)
    print("Realy End")
