import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
servo1 = GPIO.PWM(11, 50)
servo1.start(0)
time.sleep(2)

try:
    # Move to 90 degrees
    print("Moving to 90 degrees")
    servo1.ChangeDutyCycle(7)  # 90 degrees
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    time.sleep(10)  # Wait for 10 seconds

    # Move back to 0 degrees
    print("Moving back to 0 degrees")
    servo1.ChangeDutyCycle(2)  # back to0 degrees
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)

except KeyboardInterrupt:
    print("Operation interrupted by User")

finally:
    servo1.stop()
    GPIO.cleanup()
    print("Goodbye")
