import RPi.GPIO as GPIO
import time


def SendNeutralThrottle(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.setwarnings(False)

    p = GPIO.PWM(pin, 50)
    p.start(0)
    p.ChangeDutyCycle(3)

    input("press enter to quit)

    p.stop
    GPIO.cleanup()
          
