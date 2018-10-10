## Author: Feiyang jin
## Email: feiyang.jin@wustl.edu
## Organization: Washington University in St. Louis
## Date: July 2018
import serial
import pigpio
import time
import struct

floatHeader = 35

pi = pigpio.pi()
arduino = pi.serial_open("/dev/ttyACM0",19200)


def readFloat():
    while pi.serial_data_available(arduino) < 3:
        i = 1

    #serial allows us to read 4 bytes directly
    (count,data) = pi.serial_read(arduino,4)
    result = struct.unpack('f', bytes([data[3],data[2],data[1],data[0]]))
    print("we received a float",result[0])


def sendFloat(floatData):
    binary = struct.pack('f',floatData)
    pi.serial_write(arduino,[floatHeader,binary[0],binary[1],binary[2],binary[3]])



def communicate():
    while True:
        var = float(input("Please enter a float "))
        if not var:
            continue
        sendFloat(var)
        time.sleep(1)


        if pi.serial_data_available(arduino) > 0:
            inputByte = pi.serial_read_byte(arduino)
            if inputByte == floatHeader:
                readFloat()



if __name__ == '__main__':
   try:
      communicate()
   except Exception as e:
      print("Exception message:" + str(e))
      pi.serial_close(arduino)
      pi.stop()
