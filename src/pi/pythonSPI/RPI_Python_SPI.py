import spidev
import RPi.GPIO as GPIO
import time
import sys

CS = 18

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

def sendCommand(one,two):
    try:
        GPIO.output(CS,GPIO.LOW)
        val1 = spi.xfer(one)
        val2 = spi.xfer(two)
        GPIO.output(CS,GPIO.HIGH)
        print(val1)
        print(val2) 
    except:
        GPIO.cleanup()
        sys.exit(0)

def sendPWM():
    GPIO.output(CS,GPIO.LOW)
    val1 = spi.xfer(SEND_PWM)
    val2 = spi.xfer(pwm)
    print(val1)
    print(val2)
    GPIO.output(CS,GPIO.HIGH)

def sendServoAngle():
    GPIO.output(CS,GPIO.LOW);
    val1 = spi.xfer(SEND_SERVO)
    val2 = spi.xfer(servo)
    print(val1)
    print(val2)
    GPIO.output(CS,GPIO.HIGH)

while True:
    sendPWM()
    time.sleep(1)
    sendServoAngle()
    time.sleep(1)


    





