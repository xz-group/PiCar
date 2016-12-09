import smbus

from LSM9DS1 import *
import time
import datetime
import math
import sys
bus = smbus.SMBus(1)

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.00875  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      # Complementary filter constant

#adding a Logger to write to file
class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)


# define the ACC, MAG, and GRY
def writeACC(register,value):
        bus.write_byte_data(ACC_ADDRESS , register, value)
        return -1

def writeMAG(register,value):
        bus.write_byte_data(MAG_ADDRESS, register, value)
        return -1

def writeGRY(register,value):
        bus.write_byte_data(GYR_ADDRESS, register, value)
        return -1

#Define ACC reading methods first
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


#define GYR reading methods first
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


#define read Temp methods
def readTemp():
        Temp_L = bus.read_byte_data(GYR_ADDRESS,OUT_TEMP_L)
        Temp_H = bus.read_byte_data(GYR_ADDRESS,OUT_TEMP_H)
        Temp_combined = (Temp_L | Temp_H <<8)

        return Temp_combined if Temp_combined < 32768 else Temp_combined - 65536

#initialise the accelerometer
writeACC(CTRL_REG5_XL, 0b00111000) #z,y,x axis enabled, continuos update,  100Hz data rate
writeACC(CTRL_REG6_XL, 0b00000000) #+/- 4G full scale

#initialise the gyroscope
writeGRY(CTRL_REG1_G, 0b01000000) #Normal power mode, all axes enabled
writeGRY(CTRL_REG4, 0b00111000) #Continuos update, 245 dps full scale

#initialise the magnetometer
writeMAG(CTRL_REG1_M, 0b11011101) #Temp enable, M data rate = 50Hz
writeMAG(CTRL_REG2_M, 0b00000000) #+/-4gauss
writeMAG(CTRL_REG3_M, 0b00000000) #Continuous-conversion mode

gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0

a = datetime.datetime.now()
sys.stdout = Logger("IMU-log.txt")

while True:

    #Read the accelerometer,gyroscope and magnetometer values
	ACCx = readACCx()
	ACCy = readACCy()
	ACCz = readACCz()
	GYRx = readGYRx()
	GYRy = readGYRy()
	GYRz = readGYRz()
	Temp = readTemp()

    ##Calculate loop Period(LP). How long between Gyro Reads
	b = datetime.datetime.now() - a
	a = datetime.datetime.now()
	LP = b.microseconds/(1000000*1.0)
#	print "Loop Time | %5.2f|" % ( LP ),


    #Convert Gyro raw to degrees per second
	rate_gyr_x =  GYRx * G_GAIN
	rate_gyr_y =  GYRy * G_GAIN
	rate_gyr_z =  GYRz * G_GAIN

    #Calculate the angles from the gyro.
	gyroXangle+=rate_gyr_x*LP
	gyroYangle+=rate_gyr_y*LP
	gyroZangle+=rate_gyr_z*LP

    #Convert Accelerometer values to degrees
	AccXangle =  (math.atan2(ACCy,ACCz)+M_PI)*RAD_TO_DEG
	AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG

    #convert the values to -180 and +180
	AccXangle -= 180.0
	if AccYangle > 90:
		AccYangle -= 270.0
	else:
		AccYangle += 90.0


    #Complementary filter used to combine the accelerometer and gyro values.
	CFangleX=AA*(CFangleX+rate_gyr_x*LP) +(1 - AA) * AccXangle
	CFangleY=AA*(CFangleY+rate_gyr_y*LP) +(1 - AA) * AccYangle


    #Normalize accelerometer raw values.
	accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
	accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)


        if 0:
            print "\n Time: %s" %time.time()
        if 1:
            print("\n##### X = %f G  #####" % ((ACCx * 0.224)/1000/3.55)),
            print(" Y =   %fG  #####" % ((ACCy * 0.224)/1000/3.55)),
            print(" Z =  %fG  #####" % ((ACCz * 0.224)/1000/3.55))

        if 0:
            print("\n##### GYRX,GYRY, GYRZ = %f %f %f  #####" % (GYRx, GYRy, GYRz))

        if 0:			#Change to '0' to stop showing the angles from the accelerometer
            print ("\033[1;34;40mACCX Angle %5.2f ACCY Angle %5.2f  \033[0m  \n" % (AccXangle, AccYangle)),

        if 0:			#Change to '0' to stop  showing the angles from the gyro
            print ("\033[1;31;40m\tGRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f \n" % (gyroXangle,gyroYangle,gyroZangle)),

        if 0:			#Change to '0' to stop  showing the angles from the complementary filter
            print ("\033[1;35;40m   \tCFangleX Angle %5.2f \033[1;36;40m  CFangleY Angle %5.2f \33[1;32;40m \n" % (CFangleX,CFangleY)),

        if 0:
            print("\n temperature : " +str((Temp/16.)+25.0)),

        #slow program down a bit, makes the output more readable
        time.sleep(0.1)
