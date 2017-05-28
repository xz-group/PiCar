import spidev
import RPi.GPIO as GPIO
from time import sleep
import sys

SLAVE_SELECT = 22

spi = spidev.SpiDev()
spi.open(0,0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(SLAVE_SELECT,GPIO.OUT)

test = [1]

while True:
    GPIO.output(SLAVE_SELECT,GPIO.LOW)
    val1 = spi.xfer(test)
    sleep(.001)
    GPIO.output(SLAVE_SELECT,GPIO.HIGH)
    print(val1)
