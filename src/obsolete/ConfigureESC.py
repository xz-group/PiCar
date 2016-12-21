import RPi.GPIO as GPIO
import time


def ConfigureESC(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.setwarnings(False)
    
    p = GPIO.PWM(pin, 50)
    p.start(0)

    p.ChangeDutyCycle(10)
    
    ctrl = input("Press enter to continue")
    p.ChangeDutyCycle(6)
    time.sleep(2.5)

    p.ChangeDutyCycle(8)
    time.sleep(2.5)

    p.stop()
