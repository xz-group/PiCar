import spidev
import RPi.GPIO as GPIO
import time
import sys

CS = 18
spi = spidev.SpiDev()
spi.open(0,0)
to_send = [255]

while True:
    val1 = spi.xfer(to_send)
    print(val1)

