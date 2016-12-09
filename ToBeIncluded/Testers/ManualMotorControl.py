##
## Author: Reese Frerichs
##
## Allows a user to manually control two Motors 
## Use arrow keys (asdw) to increase or decrease the speed of one or both
## Must press enter after each keystroke
## Prints duty cycle after each change.
##
## Other key options: 'max' = max speed, 'min' = min speed, 'n' = neutral
##
## Update motor parameters for throttle dead band, or leave as 7.5,7.5,2.5,pin,pi
## to access true min (5%) and max(10%) values for configuring or programming ESC
##
##========================================================================##
## CAUTION: NEVER SEND MAX (10%) OR MIN(5%) dc TO ESC WITH A WHEEL ATTACHED
## THE WHEEL WILL ROTATE TOO FAST AND EXPLODE
## ONLY USE TRUE MAX AND MIN FOR CONFIGURING AND PROGRAMMING
##========================================================================##


import time
import RPi.GPIO as GPIO
import pigpio
import sys
sys.path.append("/home/pi/RPi-Test-Files/ToBeIncluded/Objects")
from Motor import Motor
    

def ManualMotorControl(pin1, pin2):
    #pin must be 12, 13, 18, or 19

    running = True

    Frequency = 50
    
    MaxSpeed = 100
    MinSpeed = -100
     
    pi = pigpio.pi()

    Left = Motor(7.5, 7.5, 2.5, pin1, pi) #FIXME: update for throttle dead band
    Right = Motor(7.5,7.5,2.5,pin2, pi)   #(use FindMinSpeeds)
    
    
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
