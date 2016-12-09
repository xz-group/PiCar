import pigpio
import time
import RPi.GPIO as GPIO
from Motor import Motor
from Encoder import Encoder
from SpeedController import SpeedController

def SpeedControlTest(pin):

    pi = pigpio.pi()

    LeftMotor = Motor(7.7475,7.265,0.01,pin,pi)
    LeftEncoder = Encoder(6,13)
    
    LeftSpeedController = SpeedController(LeftMotor, LeftEncoder, 0)

    ctrl = raw_input("Press enter to continue")
    
    while True:
        LeftSpeedController.setSpeed(3)
        x,v = LeftEncoder.sample()
        print(LeftMotor.calcDutyCycle(LeftMotor.speed), LeftSpeedController.pid.output,v)

    
