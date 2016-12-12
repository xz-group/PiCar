## IMU Object
## Uses accelerometer, magnetometer, and gyro
## This IMU object has commented out code if one would like to add readings of the other accelerometer and gyro angles as well as magnetometer readings

import smbus
from LSM9DS1 import *
import time
import datetime
import math
import sys
import socket

#adding a Logger to write to file
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

##        #initialise the magnetometer
##        self.writeMAG(CTRL_REG1_M, 0b11011101) #Temp enable, M data rate = 50Hz
##        self.writeMAG(CTRL_REG2_M, 0b00000000) #+/-4gauss
##        self.writeMAG(CTRL_REG3_M, 0b00000000) #Continuous-conversion mode

        self.PrevTime = time.time()
        self.gyroZangle = 0.0
##        gyroXangle = 0.0
##        gyroYangle = 0.0
        self.Vo = 0.0

    # define the ACC, MAG, and GRY
    def writeACC(self, register,value):
            bus.write_byte_data(ACC_ADDRESS , register, value)
            return -1

##    def writeMAG(self, register,value):
##            bus.write_byte_data(MAG_ADDRESS, register, value)
##            return -1

    def writeGRY(self, register,value):
            bus.write_byte_data(GYR_ADDRESS, register, value)
            return -1

    #Define ACC reading methods first
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


    #define GYR reading methods first
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

    def sample(self):
        currTime = time.time()
        timeDiff = currTime - self.PrevTime
        LP = timeDiff
        self.PrevTime = currTime



         #Read the accelerometer,gyroscope and magnetometer values
##        ACCx = self.readACCx()
        ACCy = self.readACCy()
##        ACCz = self.readACCz()


##        GYRx = self.readGYRx()
##        GYRy = self.readGYRy()
        GYRz = self.readGYRz()


        Temp = self.readTemp()

        #Convert Gyro raw to degrees per second
##        rate_gyr_x =  GYRx * G_GAIN
##        rate_gyr_y =  GYRy * G_GAIN
        rate_gyr_z =  GYRz * G_GAIN

        #Calculate the angles from the gyro.
##        gyroXangle+=rate_gyr_x*LP
##        gyroYangle+=rate_gyr_y*LP
        self.gyroZangle+=rate_gyr_z*LP

##        #Convert Accelerometer values to degrees
##        AccXangle =  (math.atan2(ACCy,ACCz)+M_PI)*RAD_TO_DEG
##        AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG
##
##        #convert the values to -180 and +180
##        AccXangle -= 180.0
##        if AccYangle > 90:
##            AccYangle -= 270.0
##        else:
##            AccYangle += 90.0

##        #Complementary filter used to combine the accelerometer and gyro values.
##        CFangleX=AA*(CFangleX+rate_gyr_x*LP) +(1 - AA) * AccXangle
##        CFangleY=AA*(CFangleY+rate_gyr_y*LP) +(1 - AA) * AccYangle
##
##
##        #Normalize accelerometer raw values.
##        accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
##        accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
##
        #Calculate ACC in G
##        X_G = (ACCx * 0.061)/1000
        Y_G = (ACCy * 0.061)/1000
##        Z_G = (ACCz * 0.061)/1000
        ACCy = (int((Y_G+ 0.0015)*1000)*1.0)/1000
        V = self.Vo + (ACCy)*9.8*LP

        self.Vo = V
        if 1:
            print "Time | %5.4f| Loop Time | %5.4f| \n" % (self.PrevTime, LP ),
        if 1:
            print "Velocity = | %f| GyroZAngle = | %f| \n" % (self.Vo, self.gyroZangle ),
##
##        if 0:
##            print("\n##### X_G, Y_G, Z_G = %f %f %f  #####\n" % (X_G, Y_G, Z_G))
##
##        if 0:
##            print("\n##### GYRX,GYRY, GYRZ = %f %f %f  #####\n" % (GYRx, GYRy, GYRz))
##
##        if 0:           #Change to '0' to stop showing the angles from the accelerometer
##            print ("\033[1;34;40mACCX Angle %5.2f ACCY Angle %5.2f  \033[0m  \n" % (AccXangle, AccYangle))

##        if 0:           #Change to '0' to stop  showing the angles from the gyro
##            print ("\033[1;31;40m\tGRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f \n" % (gyroXangle,gyroYangle,gyroZangle)),

        return V, self.gyroZangle

    def setIMUVelocity(self, R_enc_vel, L_enc_vel):
        averageVel = 0.5*R_enc_vel + 0.5*L_enc_vel
        if((averageVel < 0.05) and (averageVel > -0.05)):
            self.Vo = 0
        
