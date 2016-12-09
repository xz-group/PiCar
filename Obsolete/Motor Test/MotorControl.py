import Pulse
running = True
speed = 1.5

print("w: speed up|s: speed down|q:quit")

while(running):
    Pulse.Pulse(100,speed,17)
    try:
        ctrl = input()
    except:
        1+1
    
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
        running = False;
    else:
        print(speed)
