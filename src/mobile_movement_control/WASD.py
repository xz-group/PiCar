"""This program allows for complete control of the PiCar's movement 
and data collection using the keyboard"""
from devices_int import getSensorAndCamera
from multiprocessing import Process
from comms import I2C
import curses
import smbus
import time
import subprocess

i2c = I2C()
get = Process(target = getSensorAndCamera, args = ("192.168.1.121",6000,False,
             5,True,6,6,7,2,245,4,5,50,50,0.001,))
# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.noecho()
curses.cbreak()
screen.scrollok(True)
#curses.halfdelay(1)
screen.keypad(True)
start_time = 0
flag = True
right_counter = 0
left_counter = 0
command = 0
data_flag = 0
commands = []
times = []
x = 0
first_flag = 1

try:
        screen.addstr("CONTROLS:\n", curses.color_pair(1))
        screen.addstr("ONLY PRESS THE BUTTON, DO NOT HOLD\n", 
                     curses.color_pair(1))
        screen.addstr("W - Forward\n", curses.color_pair(1))
        screen.addstr("A - Left\n", curses.color_pair(1))
        screen.addstr("S - Reverse\n", curses.color_pair(1))
        screen.addstr("D - Right\n", curses.color_pair(1))
        screen.addstr("X - Start/Stop Data Logging\n", curses.color_pair(1))
        screen.addstr("Q - Quit Out Of Program\n", curses.color_pair(1))
        screen.addstr("R - Replay Last Run While Data Was Being Collected\n", curses.color_pair(1))
        screen.addstr("Any Other Button - Stop\n", curses.color_pair(1))
        screen.addstr("COMMAND HISTORY\n", curses.A_UNDERLINE)

        while True:

            char = screen.getch()
            elapsed_time = time.time() - start_time
            start_time = time.time()

            if char != ord('d'):
                right_counter = 0

            if char != ord('a'):
                left_counter = 0

            if (data_flag == 1 and first_flag == 0):
                times.append(elapsed_time)

            if (data_flag == 1):
               first_flag = 0

            if char == ord('q'):
                i2c.writeNumber(5)
                screen.addstr(str("{0:.3f}".format(elapsed_time)) + " seconds")
                break

            elif char == ord('w'):
                if (data_flag == 1):
                    commands.append(1)
                if (command == 0):
                    screen.addstr("Forward ")
                else:
                    screen.addstr(str("{0:.3f}".format(elapsed_time)) + " seconds\n" + "Forward ")
                i2c.writeNumber(1)

            elif char == ord('s'):
                if (data_flag == 1):
                    commands.append(2)
                if (command == 0):
                    screen.addstr("Reverse ")
                else:
                    screen.addstr(str("{0:.3f}".format(elapsed_time)) + " seconds\n" + "Reverse ")
                i2c.writeNumber(2)

            elif char == ord('d'):
                if (data_flag == 1):
                    commands.append(3)
                if (right_counter != 3):
                    right_counter += 1
                if (right_counter == 1):
                    if (command == 0):
                        screen.addstr("Right(1) ")
                    else:
                        screen.addstr(str("{0:.3f}".format(elapsed_time)) + " seconds\n" +  "Right(1) ")
                elif (right_counter == 2):
                    screen.addstr(str("{0:.3f}".format(elapsed_time)) + " seconds\n" +  "Right(2) ")
                elif (right_counter == 3):
                    screen.addstr(str("{0:.3f}".format(elapsed_time)) + " seconds\n" +  "Right(3) ")
                i2c.writeNumber(3)

            elif char == ord('a'):
                if (data_flag == 1):
                    commands.append(4)
                if (left_counter != 3):
                    left_counter += 1
                if (left_counter == 1):
                    if (command == 0):
                        screen.addstr("Left(1) ")
                    else:
                        screen.addstr(str("{0:.3f}".format(elapsed_time)) + " seconds\n" + "Left(1) ")
                elif (left_counter == 2):
                    screen.addstr(str("{0:.3f}".format(elapsed_time)) + " seconds\n" + "Left(2) ")
                elif (left_counter == 3):
                    screen.addstr(str("{0:.3f}".format(elapsed_time)) + " seconds\n" + "Left(3) ")
                i2c.writeNumber(4)

            elif char == ord('x'):
                if flag:
                    if (command == 0):
                        screen.addstr("Data Recording Has Started ")
                    else:
                        screen.addstr(str("{0:.3f}".format(elapsed_time)) + " seconds\n" + "Data Recording Has Started ")
                    get = Process(target = getSensorAndCamera, args = ("192.168.1.121",6000,False,
                    5,True,6,6,7,2,245,4,5,50,50,0.001,))
                    get.start()
                    flag = False
                    data_flag = 1
                    commands.clear()
                    times.clear()
                else:
                    screen.addstr(str("{0:.3f}".format(elapsed_time)) + " seconds\n" + "Data Recording Has Stopped ")
                    get.terminate()
                    for i in commands:
                        screen.addstr("\n" + str(i))
                    screen.addstr("\n")
                    for t in times:
                        screen.addstr(str(t) + "\n")
                    flag = True
                    data_flag = 0
                    first_flag = 1

            elif char == ord('r'):
                x = 0
                screen.addstr(str("{0:.3f}".format(elapsed_time)) + " seconds\n" + "Replaying...\n")
                screen.refresh()
                get = Process(target = getSensorAndCamera, args = ("192.168.1.121",6000,False,
                5,True,6,6,7,2,245,4,5,50,50,0.001,))
                get.start()
                while (x < len(commands)):
                    i2c.writeNumber(commands[x])
                    time1 = time.time()
                    time.sleep(times[x])
                    time2 = time.time() - time1
                    screen.addstr(str(time2) + "\n")
                    x += 1
                screen.addstr("Replay Complete! ")
                get.terminate()

            else:
                if (data_flag == 1):
                    commands.append(5)
                if (command == 0):
                    screen.addstr("Stop ")
                else:
                    screen.addstr(str("{0:.3f}".format(elapsed_time)) + " seconds\n" + "Stop ")
                i2c.writeNumber(5)

            command = 1
finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()

