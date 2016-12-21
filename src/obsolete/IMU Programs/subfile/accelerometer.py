#!/usr/bin/python
#    Copyright (C) 2016  Mark Williams
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Library General Public
#    License as published by the Free Software Foundation; either
#    version 2 of the License, or (at your option) any later version.
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    Library General Public License for more details.
#    You should have received a copy of the GNU Library General Public
#    License along with this library; if not, write to the Free
#    Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
#    MA 02111-1307, USA


import smbus
from LSM9DS1 import *
import time
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



while True:


	#Read the accelerometer,gyroscope and magnetometer values
	ACCx = readACCx()
	ACCy = readACCy()
	ACCz = readACCz()
# car head y direction
	print("##### X = %f G  #####" % ((ACCx * 0.061)/1000)),
	print(" Y =   %fG  #####" % ((ACCy * 0.061)/1000)),
	print(" Z =  %fG  #####" % ((ACCz * 0.061)/1000))



	#slow program down a bit, makes the output more readable
	time.sleep(0.1)
