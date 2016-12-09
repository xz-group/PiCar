import time
import RPi.GPIO as GPIO
import threading
from time import sleep
import math
import smbus
from LSM9DS1 import *
import datetime
bus = smbus.SMBus(1)


Enc_R_A = 26
Enc_R_B = 19
Enc_L_A = 6
Enc_L_B = 13

Rotary_counter_L = 0
Rotary_counter_R = 0
Current_R_A = 1               
Current_R_B = 1
Current_L_A = 1               
Current_L_B = 1

PrevTime_L = time.time()
PrevTime_R = time.time()
T =0
Velocity_L = 0
Velocity_R = 0

LockRotary_R = threading.Lock()
LockRotary_L = threading.Lock()

bus = smbus.SMBus(1)

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.00875  # [deg/s/LSB] 

def writeACC(register,value):
   bus.write_byte_data(ACC_ADDRESS , register, value)
   return -1

def readACCx():
   acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_X_L_XL)
   acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_X_H_XL)
   acc_combined = (acc_l | acc_h <<8)
   return acc_combined  if acc_combined < 32768 else acc_combined - 65536

def readACCy():
   acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Y_L_XL)
   acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Y_H_XL)
   acc_combined = (acc_l | acc_h <<8)
   return acc_combined  if acc_combined < 32768 else acc_combined - 65536

def readACCz():
   acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Z_L_XL)
   acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Z_H_XL)
   acc_combined = (acc_l | acc_h <<8)
   return acc_combined  if acc_combined < 32768 else acc_combined - 65536


#initialise the accelerometer
writeACC(CTRL_REG5_XL, 0b00010000) #y axis enabled, continuos update,  50Hz data rate
writeACC(CTRL_REG6_XL, 0b01000000) #+/- 2 full scale

def writeGRY(register,value):
        bus.write_byte_data(GYR_ADDRESS, register, value)
        return -1


def readGYRx():
        gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_X_L_G)
        gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_X_H_G)
        gyr_combined = (gyr_l | gyr_h <<8)

        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536


def readGYRy():
        gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Y_L_G)
        gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Y_H_G)
        gyr_combined = (gyr_l | gyr_h <<8)

        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536

def readGYRz():
        gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Z_L_G)
        gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Z_H_G)
        gyr_combined = (gyr_l | gyr_h <<8)

        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536
      
#initialise the gyroscope
writeGRY(CTRL_REG1_G, 0b01000000) #245dps
writeGRY(CTRL_REG4, 0b00100000) #z axis



def rotary_interrupt_left(A_or_B):
   #True for Left, False for Right
   global Rotary_counter_L, Current_L_A, Current_L_B, LockRotary_L, T_L, PrevTime_L, Velocity_L
                                       # read both of the switches
   Switch_L_A = GPIO.input(Enc_L_A)
   Switch_L_B = GPIO.input(Enc_L_B)
   
                                       # now check if state of A or B has changed
                                       # if not that means that bouncing caused it
   if Current_L_A == Switch_L_A and Current_L_B == Switch_L_B:      # Same interrupt as before (Bouncing)?
      return                              # ignore interrupt!

   Current_L_A = Switch_L_A                        # remember new state
   Current_L_B = Switch_L_B                        # for next bouncing check

   
   if (Switch_L_A and Switch_L_B):                  # Both ones active? Yes -> end of sequence
      LockRotary_L.acquire()                  # get lock

      T_L = time.time()-PrevTime_L
      if(T_L != 0):
         Velocity_L = 0.056 * 3.14159 / (400*T_L)
      else:
         Velocity_L = 0

      
      
      if A_or_B == Enc_L_A:                     # Turning direction depends on
         Rotary_counter_L += 1                  # which input gave last interrupt
      else:                              # so depending on direction either
         Rotary_counter_L -= 1                  # increase or decrease counter
         Velocity_L = Velocity_L * -1
 
      PrevTime_L = time.time() 
      LockRotary_L.release()                  # and release lock
      
   return

def rotary_interrupt_right(A_or_B):
   #True for Left, False for Right
   global Rotary_counter_R, Current_R_A, Current_R_B, LockRotary_R, T_R, PrevTime_R, Velocity_R
                                       # read both of the switches
   Switch_R_A = GPIO.input(Enc_R_A)
   Switch_R_B = GPIO.input(Enc_R_B)
   
                                       # now check if state of A or B has changed
                                       # if not that means that bouncing caused it
   if Current_R_A == Switch_R_A and Current_R_B == Switch_R_B:      # Same interrupt as before (Bouncing)?
      return                              # ignore interrupt!

   Current_R_A = Switch_R_A                        # remember new state
   Current_R_B = Switch_R_B                        # for next bouncing check

   
   if (Switch_R_A and Switch_R_B):                  # Both ones active? Yes -> end of sequence
      LockRotary_R.acquire()                  # get lock

      T_R = time.time()-PrevTime_R
      if(T_R != 0):
         Velocity_R = 0.056 * 3.14159 / (400*T_R)
      else:
         Velocity_R = 0


      
      
      if A_or_B == Enc_R_B:                     # Turning direction depends on
         Rotary_counter_R += 1                  # which input gave last interrupt
      else:                              # so depending on direction either
         Rotary_counter_R -= 1                  # increase or decrease counter
         Velocity_R = Velocity_R * -1
 
      PrevTime_R = time.time() 
      LockRotary_R.release()                  # and release lock
      
   return 


def init():
   GPIO.setwarnings(False)
   GPIO.setmode(GPIO.BCM)               # Use BCM mode
                                 # define the Encoder switch inputs
   GPIO.setup(Enc_R_A, GPIO.IN)
   GPIO.setup(Enc_R_B, GPIO.IN)
   GPIO.setup(Enc_L_A, GPIO.IN)
   GPIO.setup(Enc_L_B, GPIO.IN)
   
                                 # setup callback thread for the A and B encoder
                                 # use interrupts for all inputs
   GPIO.add_event_detect(Enc_R_A, GPIO.RISING, callback=rotary_interrupt_right)             # NO bouncetime
   GPIO.add_event_detect(Enc_R_B, GPIO.RISING, callback=rotary_interrupt_right)
   GPIO.add_event_detect(Enc_L_A, GPIO.RISING, callback=rotary_interrupt_left)             # NO bouncetime
   GPIO.add_event_detect(Enc_L_B, GPIO.RISING, callback=rotary_interrupt_left) 
   return

def main():

   global Rotary_counter_L, Rotary_counter_R, LockRotary_R, LockRotary_L, rate_gyr_z

   NewCounter = 0                        # for faster reading with locks
   init()                              # Init interrupts, GPIO, ...
   Vo = 0
   a = datetime.datetime.now()
   gyroZangle = 0.0

   while True :                        # start test
      sleep(0.2)                        # sleep 200 msec

      LockRotary_L.acquire()               
      NewCounter_L = Rotary_counter_L
      V_L = Velocity_L
      LockRotary_L.release()

      LockRotary_R.acquire()               
      NewCounter_R = Rotary_counter_R
      V_R = Velocity_R
      LockRotary_R.release()
      ################################
      #set IMU V0 = 0 if Encoder doesn't read anything
      if (V_R > -0.05)&(V_R <0.05):
         Vo = 0;

        ##Calculate loop Period(LP). How long between Reads
      b = datetime.datetime.now() - a
      a = datetime.datetime.now()
      LP = b.microseconds/(1000000*1.0)

	#Read the y axis accelerometer
      ACCy = readACCy()*0.061/10000
#      print("\n Y =   %fG  " % (ACCy))

      #########calibration
      ACCy = (int((ACCy+ 0.0015)*1000)*1.0)/1000
#      print("\n Y =   %fG  " % (ACCy))
      
      #calculate velocity
      V = Vo + (ACCy)*9.8*LP
      Vo = V
      # average velocity
      average_V = 0.50 * V_R + 0.50 * V
##################################
      #not accurate
      #read gyro
      GYRz = readGYRz()
      rate_gyr_z =  GYRz * G_GAIN
      #calculate angle
      gyroZangle+=rate_gyr_z*LP
      
#      print ("Left Distance = " + str(NewCounter_L*0.056*3.14159/400) + "Left Velocity = " + str(V_L))        
#      print ("Right Distance = " + str(NewCounter_R*0.056*3.14159/400))
#      print("Encoder Right Velocity = " + str(V_R))

#      print("\n Y =   %fG  " % (ACCy))
      print(" IMU Velocity= %f m/s" % (V))
#      print("   average_V = %f\n" %(average_V))

      print(" rate =  %f  \n" % (rate_gyr_z))
      print(" angle =  %f  \n" % (gyroZangle))
      
main()
