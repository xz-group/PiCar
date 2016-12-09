## Use to find edges of throttle dead band.
## Author: Reese Frerichs
##
##
## How To:
##
## 1. Enter the following command in Command Line: sudo pigpiod
## 2. Conenct ESC to Motor, battery, and RPi PWM; secure motor (e.g. vice grip).
## 3. Estimate starting speed; set speed to that guess in FIXME1.
##      7.6 is a good start for forward; 7.4 for reverse
## 4. Choose direction and precision.  Update FIXME2:
##      Change sign to + for forward, - for reverse.
##      0.05 is a good starting precision; decrease on each iteration.
## 5. Run script (Python 2).
## 6. Turn ESC on.  Wait for *Ring* + Beep-Beep + *Ring* *Ring*.
##      *Ring* is 4 Descending Tones
## 7. Press enter in shell to continue.
## 8. Wait until motor begins to turn; make note of minimum speed before it turns
##      If performing more iterations for increased precision, use this value
##      as the new guess in FIXME1.
## 9. Repeat with greater precision until satisfactory precision is achieved.
##

import pigpio
import time
import RPi.GPIO as GPIO


def FindMinSpeeds(pin):    
    Frequency = 50
    
    MaxSpeed = 0.2*Frequency
    MinSpeed = 0.1*Frequency
    Neutral = 0.15*Frequency
    
    speed = Neutral                             #Waits at neutral throttle

    pi = pigpio.pi()
    pi.hardware_PWM(pin, Frequency, speed*10000)

    ctrl = raw_input("Press enter to continue") #Wait until ESC is powered on

    speed = 7.7                               ##FIXME1: Initial Speed Guess                       
    for i in range (0,100,1):
        speed = speed + 0.01                    ##FIXME2: Direction and Precision

        pi.hardware_PWM(pin, Frequency, speed*10000)
        print(speed)
        time.sleep(2)


