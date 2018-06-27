## IMU Object
## Uses accelerometer and gyro from a LSM9DS1 IMU
## Samples the Y acceleration and Z gyro angle as well as temperature (if needed)
## If you want to sample other axis from the accelerometer, gyro, or magnetometer,
## use the file IMU-old.py from the Archived -> Obsolete file folder
## This class object was developed from a modification of the BerryIMU programs

import smbus
from LSM9DS1 import *
import time
import datetime
import math
import sys
import socket

#adding a Logger to write to file if you want to save data
class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

class IMU(object):
    global bus, RAD_TO_DEG, M_PI, G_GAIN, AA, PrevTime
    PrevTime = 0
    bus = smbus.SMBus(1)
    RAD_TO_DEG = 57.29578
    M_PI = 3.14159265358979323846
    G_GAIN = 0.00875  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
    AA =  0.40      # Complementary filter constant


    def __init__(self):


        #initialise the accelerometer
        self.writeACC(CTRL_REG5_XL, 0b00111000) #z,y,x axis enabled, continuos update,  100Hz data rate
        self.writeACC(CTRL_REG6_XL, 0b00000000) #+/- 2G full scale

        #initialise the gyroscope
        self.writeGRY(CTRL_REG1_G, 0b01000000) #245 dps
        self.writeGRY(CTRL_REG4,   0b00100000) #z axis

        self.PrevTime = time.time()
        self.gyroZangle = 0.0 # only measuring gyro Z angle
        self.Vo = 0.0   #Initial velocity


    # define the ACC and GRY
    def writeACC(self, register,value):
            bus.write_byte_data(ACC_ADDRESS , register, value)
            return -1

    def writeGRY(self, register,value):
            bus.write_byte_data(GYR_ADDRESS, register, value)
            return -1


    #Define ACC reading methods
    def readACCx(self):
            acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_X_L_XL)
            acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_X_H_XL)
            acc_combined = (acc_l | acc_h <<8)

            return acc_combined  if acc_combined < 32768 else acc_combined - 65536

    def readACCy(self):
            acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Y_L_XL)
            acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Y_H_XL)
            acc_combined = (acc_l | acc_h <<8)

            return acc_combined  if acc_combined < 32768 else acc_combined - 65536

    def readACCz(self):
            acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Z_L_XL)
            acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Z_H_XL)
            acc_combined = (acc_l | acc_h <<8)

            return acc_combined  if acc_combined < 32768 else acc_combined - 65536


    #define GYR reading methods
    def readGYRx(self):
            gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_X_L_G)
            gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_X_H_G)
            gyr_combined = (gyr_l | gyr_h <<8)

            return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536

    def readGYRy(self):
            gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Y_L_G)
            gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Y_H_G)
            gyr_combined = (gyr_l | gyr_h <<8)

            return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536

    def readGYRz(self):
            gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Z_L_G)
            gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Z_H_G)
            gyr_combined = (gyr_l | gyr_h <<8)

            return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536

    #define read Temp methods
    def readTemp(self):
            Temp_L = bus.read_byte_data(GYR_ADDRESS,OUT_TEMP_L)
            Temp_H = bus.read_byte_data(GYR_ADDRESS,OUT_TEMP_H)
            Temp_combined = (Temp_L | Temp_H <<8)

            return Temp_combined if Temp_combined < 32768 else Temp_combined - 65536

    # this method is called by the main script to sample the IMU continuously
    def sample(self):
        currTime = time.time()
        timeDiff = currTime - self.PrevTime
        LP = timeDiff
        self.PrevTime = currTime

         #Read the accelerometer,gyroscope and magnetometer values

        ACCy = self.readACCy()
        GYRz = self.readGYRz()
        Temp = self.readTemp()

        #Convert Gyro raw to degrees per second
        rate_gyr_z =  GYRz * G_GAIN

        #Calculate the angles from the gyro.
        self.gyroZangle+=rate_gyr_z*LP


        #Calculate ACC in G
        Y_G = (ACCy * 0.061)/1000
        ACCy = (int((Y_G+ 0.0015)*1000)*1.0)/1000
        
        #Calculates current velocity using Loop Time
        V = self.Vo + (ACCy)*9.8*LP

        self.Vo = V
        
        #Can print for testing purposes or write to file
        if 0:
            print "Time | %5.4f| Loop Time | %5.4f| \n" % (self.PrevTime, LP ),
        if 0:
            print "Velocity = | %f| GyroZAngle = | %f| \n" % (self.Vo, self.gyroZangle ),

        return V, self.gyroZangle

    # Use this if you want to set the IMU velocity based on the Encoders' velocity
    def setIMUVelocity(self, R_enc_vel, L_enc_vel):
        averageVel = 0.5*R_enc_vel + 0.5*L_enc_vel
        if((averageVel < 0.05) and (averageVel > -0.05)):
            self.Vo = 0
        
