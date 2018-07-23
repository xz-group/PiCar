## Author: Feiyang jin
## Email: feiyang.jin@wustl.edu
## Organization: Washington University in St. Louis
## Date: July 2018

import time,pigpio,struct

pi = pigpio.pi()

if not pi.connected:
   exit(0)

h = pi.spi_open(0, 40000)


#tell arduino we are going to read a float
def getReadyForReadFloat():
   pi.spi_write(h,b'\x02')


#function that reads the float
def readFloat():

   (count1,byte1) = pi.spi_read(h,1)

   (count2,byte2) = pi.spi_read(h,1)

   (count3,byte3) = pi.spi_read(h,1)

   (count4,byte4) = pi.spi_read(h,1)

   result = struct.unpack('f', bytes([byte4[0],byte3[0],byte2[0],byte1[0]]))
   print("The float received is",result[0])


#tell arduino we are going to send a float
def getReadyForSendFloat():
   pi.spi_write(h,b'\x03')


#function that sends the float
def sendFloat(floatData):
   binary = struct.pack('f',floatData)
   for byte in binary:
      pi.spi_write(h,[byte])


#tell arduino we are going to send a int
def getReadyForSendInt():
   pi.spi_write(h,b'\x04')


#function that sends the int
def sendInt(intData):
   pi.spi_write(h,[intData])


#function for communicating with arduino
def communicate():
   while True:
      #send int to arduino
      intVar = int(input("please enter an int "))
      if not intVar:
         continue

      getReadyForSendInt()
      sendInt(intVar)

      time.sleep(1)

      #send float to arduino
      var = float(input("Please enter a float "))
      if not var:
         continue

      getReadyForSendFloat()
      sendFloat(var)

      time.sleep(1)

      getReadyForReadFloat()

      #we want to check if arduino is able to send the float
      (count,data) = pi.spi_read(h,1)
      if data[0] == 35:
         readFloat()
      elif data[0] != 35:
         print("Fail to read the float")



if __name__ == '__main__':
   try:
      communicate()
   except Exception as e:
      print("Exception message:" + str(e))
      pi.spi_close(h)
      pi.stop()
