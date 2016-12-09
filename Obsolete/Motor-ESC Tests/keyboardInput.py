import Pulse
running = True
speed = 1.5

while(running):
    Pulse.Pulse(1,speed,17)
    ctrl = input("w: speed up|s: speed down|q:quit")
    if(ctrl=="w"):
        speed = speed + 0.05
        if(speed>2):
            speed = 2
        print (speed)
    elif (ctrl=="s"):
        speed = speed - 0.01
        if(speed<1):
            speed = 1;
        print (speed)
    elif(ctrl=="q"):
        running = false;
    else:
        print(speed)
