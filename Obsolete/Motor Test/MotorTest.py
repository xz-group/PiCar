import time
import RPi.GPIO as GPIO

def MotorTest(pin):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.setwarnings(False)

    running = True
    speed = 8
    
    p = GPIO.PWM(pin, 50) 
    p.start(0)


    p.ChangeDutyCycle(speed)
    
    while(running):
        ctrl = input("w: speed up.  s: slow down.  q:quit")
        if(ctrl=="w"):
            speed = speed+0.05
        elif(ctrl=="p1"):
            speed = speed+1
        elif(ctrl=="m1"):
            speed = speed-1
        elif(ctrl=="s"):
            speed = speed-0.05
        elif(ctrl=="q"):
             running = False
        elif(ctrl=="max"):
            speed = 10
        elif(ctrl=="min"):
            speed = 6
        elif(ctrl=="n"):
            speed = 8
        print(speed)
        p.ChangeDutyCycle(speed)         

    p.stop()

