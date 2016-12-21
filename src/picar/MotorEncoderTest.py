## Measures Encoder data while controlling a motor.
## Only testing for Left Encoder and Left Motor 


import pigpio
import time
import RPi.GPIO as GPIO
import sys
#sys.path.append("/home/pi/PiCarAPI/ToBeIncluded/Objects")
from Motor import Motor
from Encoder import Encoder

def MotorEncoderTest(pin):
    pi = pigpio.pi()
    
    LeftMotor = Motor(7.7475,7.265,0.05,pin,pi)  
    LeftMotor.setSpeed(0)

    LeftEncoder = Encoder(6,13)

    speedDecreaser = 10
    ctrl = raw_input("Press enter to continue")

    for i in range (1,5,1):

        LeftMotor.setSpeed(i)
        time.sleep(3)
        
        print("Speed: " + str(LeftMotor.speed) + " PWM: " + str(LeftMotor.calcDutyCycle(LeftMotor.speed)))
        for j in range (0,150,1):

            if j%speedDecreaser==0:
                LeftMotor.setSpeed(0)
            else:
                LeftMotor.setSpeed(i)

            x = LeftEncoder.sample()
            print (x)
            time.sleep(0.02)
        

    LeftMotor.setSpeed(0)
