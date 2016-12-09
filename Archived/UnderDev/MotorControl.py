import time
import RPi.GPIO as GPIO

def MotorControl(pin1, pin2):
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    
    running = True

    Frequency = 20
    MaxSpeed = 0.2*Frequency
    MinSpeed = 0.1*Frequency
    Neutral = 0.15*Frequency
    
    LeftSpeed = Neutral
    RightSpeed = Neutral

    RightMotor = GPIO.PWM(pin1, Frequency) 
    RightMotor.start(0)
    LeftMotor = GPIO.PWM(pin2, Frequency)
    LeftMotor.start(0)

    RightMotor.ChangeDutyCycle(LeftSpeed)
    LeftMotor.ChangeDutyCycle(RightSpeed)

    ctrl = input("After ESC startup, press any key to continue.")

    LeftSpeed = Neutral
    RightSpeed = Neutral
    RightMotor.ChangeDutyCycle(RightSpeed)
    LeftMotor.ChangeDutyCycle(LeftSpeed)
    
    while(running):
        ctrl = input("Use ASDW to navigate.")
        if(ctrl == "a"):
            LeftSpeed = LeftSpeed + 0.25
        elif(ctrl == "s"):
            LeftSpeed = LeftSpeed - 0.25
            RightSpeed= RightSpeed - 0.25
        elif(ctrl == "d"):
            RightSpeed = RightSpeed + 0.25
        elif(ctrl == "w"):
            RightSpeed = RightSpeed + 0.25
            LeftSpeed = LeftSpeed + 0.25
        elif(ctrl == "FullSpeed"):
            LeftSpeed = MaxSpeed
            RightSpeed = MaxSpeed
        elif(ctrl == "stop"):
            LeftSpeed = Neutral
            RightSpeed = Neutral
        elif(ctrl == "Reverse"):
            LeftSpeed = MinSpeed
            RightSpeed = MinSpeed
        elif(ctrl =="q"):
            running = False

        RightMotor.ChangeDutyCycle(RightSpeed)
        LeftMotor.ChangeDutyCycle(LeftSpeed)


        
        print("LeftSpeed = " + str(LeftSpeed) + "RightSpeed = " + str(RightSpeed))
        
