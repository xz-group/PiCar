import smbus
from LSM9DS1 import *
import time
import datetime
bus = smbus.SMBus(1)





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
writeACC(CTRL_REG5_XL, 0b00111000) #z,y,x axis enabled, continuos update,  100Hz data rate
writeACC(CTRL_REG6_XL, 0b00000000) #+/- 2 full scale

Vo = 0
a = datetime.datetime.now()
while True:
 ##Calculate loop Period(LP). How long between Reads
	b = datetime.datetime.now() - a
	a = datetime.datetime.now()
	LP = b.microseconds/(1000000*1.0)
	#print "Loop Time | %5.2f|" % ( LP ),

	#Read the accelerometer,gyroscope and magnetometer values
	ACCx = readACCx()*0.061/1000
	ACCy = readACCy()*0.061/1000
    	ACCz = readACCz()*0.061/1000

        #calibration
    	ACCy = (int((ACCy+ 0.018)*100)*1.0)/100
    	
        V = Vo + (ACCy)*9.8*LP
        Vo = V
        # car head y direction
	#print("##### X = %f G  #####" % (ACCx))


	print(" Y =   %fG  #####/n" % (ACCy))
	#print(" Z =  %fG  #####" % (ACCz))

        print("/n Velocity= %f m/s)" % (V))


	#slow program down a bit, makes the output more readable
	time.sleep(0.5)

