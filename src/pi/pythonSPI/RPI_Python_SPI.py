import spidev
import RPi.GPIO as GPIO
from time import sleep
import sys

CS = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(CS,GPIO.OUT)

SEND_PWM = [1]
SEND_SERVO = [2]

spi = spidev.SpiDev()
spi.open(0,0)
to_send = [-1]
something = [-1]
pwm = [30]
servo = [90]
DELAY = .01

def sendPWM():
    GPIO.output(CS,GPIO.LOW)
    val1 = spi.xfer(SEND_PWM)
    val2 = spi.xfer(pwm)
    sleep(DELAY)
    GPIO.output(CS,GPIO.HIGH)
    print(val1)
    print(val2)

def sendServoAngle():
    GPIO.output(CS,GPIO.LOW);
    val1 = spi.xfer(SEND_SERVO)
    val2 = spi.xfer(servo)
    sleep(DELAY)
    GPIO.output(CS,GPIO.HIGH)
    print(val1)
    print(val2)

while True:
    sendPWM()
    sleep(1)
    sendServoAngle()
    sleep(1)


    





