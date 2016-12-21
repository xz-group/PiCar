import RPi.GPIO as GPIO
import time

numTimes = 100
duration = 2
pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin,GPIO.OUT)

for i in range(0, numTimes):
    GPIO.output(pin, True)
    time.sleep(2/1000)
    GPIO.output(pin,False)
    time.sleep(48/1000)
