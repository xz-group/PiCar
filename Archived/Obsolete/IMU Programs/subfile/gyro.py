import smbus
import time
import math
import datetime

from LSM9DS1 import *
import time

bus = smbus.SMBus(1)

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.00875  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly


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
writeGRY(CTRL_REG4, 0b00100000) #z axis enabled

gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
a = datetime.datetime.now()

while True:


	#Read the accelerometer,gyroscope and magnetometer values
	GYRx = readGYRx()
	GYRy = readGYRy()
	GYRz = readGYRz()

	#Convert Gyro raw to degrees per second
	rate_gyr_x =  GYRx * G_GAIN
	rate_gyr_y =  GYRy * G_GAIN
	rate_gyr_z =  GYRz * G_GAIN

	##Calculate loop Period(LP). How long between Gyro Reads
	b = datetime.datetime.now() - a
	a = datetime.datetime.now()
	LP = b.microseconds/(1000000*1.0)
	print "Loop Time | %5.2f|" % ( LP ),


	#Calculate the angles from the gyro.
	gyroXangle+=rate_gyr_x*LP
	gyroYangle+=rate_gyr_y*LP
	gyroZangle+=rate_gyr_z*LP



	print("##### X = %f   #####" % (rate_gyr_x)),
	print(" Y =   %f  #####" % (rate_gyr_y)),
	print(" Z =  %f  #####" % (rate_gyr_z))


	#slow program down a bit, makes the output more readable
	time.sleep(0.3)

