import RPi.GPIO as GPIO
import time

def Pulse (numTimes, duration, pin): #duration in ms.  must be between 1 and 2
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin,GPIO.OUT)

    for i in range(0, numTimes):
        freq = 20/1000 #20 ms
        width = duration/1000
        rest = freq - width
        GPIO.output(pin, True)
        time.sleep(width)
        GPIO.output(pin,False)
        time.sleep(rest)
