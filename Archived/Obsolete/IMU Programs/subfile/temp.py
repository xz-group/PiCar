import smbus

from LSM9DS1 import *
import time
bus = smbus.SMBus(1)


def writeMAG(register,value):
        bus.write_byte_data(MAG_ADDRESS, register, value)
        return -1

def writeGRY(register,value):
        bus.write_byte_data(GYR_ADDRESS, register, value)
        return -1



def readTemp():
        Temp_L = bus.read_byte_data(GYR_ADDRESS,OUT_TEMP_L)
        Temp_H = bus.read_byte_data(GYR_ADDRESS,OUT_TEMP_H)
        Temp_combined = (Temp_L | Temp_H <<8)

        return Temp_combined if Temp_combined < 32768 else Temp_combined - 65536
    

writeMAG(CTRL_REG1_M, 0b11011101) #Temp enable, M data rate = 50Hz
writeMAG(CTRL_REG2_M, 0b00000000) #+/-4gauss
writeMAG(CTRL_REG3_M, 0b00000000) #Continuous-conversion mode

writeGRY(CTRL_REG1_G, 0b01000000) #Normal power mode, all axes enabled
writeGRY(CTRL_REG4, 0b00111000) #Continuos update, 245 dps full scale

while True:

    Temp = readTemp()
    print("temp = %f" %((Temp/16.)+25.0))

    #slow program down a bit, makes the output more readable
    time.sleep(0.1)
