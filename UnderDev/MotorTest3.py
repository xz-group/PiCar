import time
import RPi.GPIO as GPIO
import pigpio
import sys

sys.path.append("/home/pi/RPi-Test-Files/ToBeIncluded/Objects")
from Motor import Motor
    

def MotorTest3(pin1, pin2):
    #pin must be 12, 13, 18, or 19

    running = True

    Frequency = 50
    
    MaxSpeed = 100
    MinSpeed = -100
     
    pi = pigpio.pi()

    Left = Motor(7.5, 7.5, 2.5, pin1, pi)
    Right = Motor(7.5,7.5,2.5,pin2, pi)
    
    
    while(running):
        ctrl = raw_input("w: speed up.  s: slow down.  q:quit")
        if(ctrl=="w"):
            Left.setSpeed(Left.speed+1)
            Right.setSpeed(Right.speed+1)
        elif(ctrl=="s"):
            Left.setSpeed(Left.speed-1)
            Right.setSpeed(Right.speed-1)
        elif(ctrl=="q"):
            Left.setSpeed(0)
            Right.setSpeed(0)
            running = False
        elif(ctrl=="max"):
            Left.setSpeed(100)
            Right.setSpeed(100)
        elif(ctrl=="min"):
            Left.setSpeed(-100)
            Right.setSpeed(-100)
        elif(ctrl=="n"):
            Left.setSpeed(0)
            Right.setSpeed(0)
        elif(ctrl=="a"):
            Left.setSpeed(Left.speed+1)
            Right.setSpeed(Right.speed-1)
        elif(ctrl=="d"):
            Right.setSpeed(Right.speed+5)
            Left.setSpeed(Left.speed-5)
            
        print("Left DC: " + str(Left.calcDutyCycle(Left.speed)))
        print("Right DC: " + str(Right.calcDutyCycle(Right.speed)))
