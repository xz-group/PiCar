import smbus
import math

from LSM9DS1 import *
import time
bus = smbus.SMBus(1)

M_PI = 3.14159265358979323846

def writeMAG(register,value):
        bus.write_byte_data(MAG_ADDRESS, register, value)
        return -1


def readMAGx():
        mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_X_L_M)
        mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_X_H_M)
        mag_combined = (mag_l | mag_h <<8)

        return mag_combined  if mag_combined < 32768 else mag_combined - 65536


def readMAGy():
        mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Y_L_M)
        mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Y_H_M)
        mag_combined = (mag_l | mag_h <<8)

        return mag_combined  if mag_combined < 32768 else mag_combined - 65536


def readMAGz():
        mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Z_L_M)
        mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Z_H_M)
        mag_combined = (mag_l | mag_h <<8)

        return mag_combined  if mag_combined < 32768 else mag_combined - 65536


#initialise the magnetometer
writeMAG(CTRL_REG1_M, 0b11011100) #Temp enable, M data rate = 50Hz
writeMAG(CTRL_REG2_M, 0b00000000) #+/-4gauss
writeMAG(CTRL_REG3_M, 0b00000000) #Continuous-conversion mode


while True:
    
	#Read the accelerometer,gyroscope and magnetometer values
	MAGx = readMAGx()
	MAGy = readMAGy()
	MAGz = readMAGz()
	print("##### X = %f   #####" % (MAGx*0.00014)),
	print(" Y =   %f  #####" % (MAGy*0.00014)),
	print(" Z =  %f  #####" % (MAGz*0.00014))


	#Calculate heading
	heading = 180 * math.atan2(MAGy,MAGx)/M_PI

        print("/n ##### heading = %f   #####/n" % (heading))


	#slow program down a bit, makes the output more readable
	time.sleep(0.1)


