import time
import RPi.GPIO as GPIO
import pigpio
import sys
sys.path.append("/home/pi/RPi-Test-Files/ToBeIncluded/Objects")
from Motor import Motor
from Encoder import Encoder

def MoveToX (destination):

    pi = pigpio.pi()

    pin1 = 12
    pin2 = 18

    LeftMotor = Motor(7.7475,7.265,1,pin1,pi)  
    LeftMotor.setSpeed(0)
    LeftEncoder = Encoder(16,23)

    RightMotor = Motor(7.75,7.347,1,pin2,pi)  
    RightMotor.setSpeed(0)
    RightEncoder = Encoder(13,6)

    leftPosition, leftVelocity = LeftEncoder.sample()
    rightPosition, rightVelocity = RightEncoder.sample()

    print(rightPosition)
    i = 0
    speedDecreaser = 1000         #Lower speedDecreaser => Lower Speed
    ctrl = raw_input("Press enter to continue")
    
    while rightPosition < 0.8*destination:
        LeftMotor.setSpeed(10)
        RightMotor.setSpeed(10)

        if i%speedDecreaser == 0:
            LeftMotor.setSpeed(0)
            RightMotor.setSpeed(0)
        else:
            LeftMotor.setSpeed(10)
            RightMotor.setSpeed(10)

        leftPosition, leftVelocity = LeftEncoder.sample()
        rightPosition, rightVelocity = RightEncoder.sample()
        print(rightPosition, RightMotor.calcDutyCycle(RightMotor.speed))


        time.sleep(0.02)

        i+=1

    print("Here")
    
    LeftMotor.brake()
    RightMotor.brake()

    print(RightMotor.calcDutyCycle(RightMotor.speed))

    time.sleep(2)

    LeftMotor.setSpeed(0)
    RightMotor.setSpeed(0)

        
        
        
