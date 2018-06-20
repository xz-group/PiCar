import smbus
import time
import struct

bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

FloatHeader = 35
intHeader = 36


def getReadyForSendingInt():
   bus.write_byte(address,intHeader)


def sendInt(intData):
   bus.write_byte(address,intData)


def readFloat():
   #read 4 bytes of a float by read 4 times
   byte1 = bus.read_byte(address)
   byte2 = bus.read_byte(address)
   byte3 = bus.read_byte(address)
   byte4 = bus.read_byte(address)

   #convert the binary to float
   result = struct.unpack('f', bytes([byte4,byte3,byte2,byte1]))

   time.sleep(0.5)
   return result[0]


def getReadyForSendingFloat():
   bus.write_byte(address,FloatHeader)
   
   
def sentFloat(data): 
    binary = struct.pack('f',data)
    for byte in binary:
        bus.write_byte(address,byte)


def communicate():
   while True:
     #send int to arduino
     intVar = int(input("Enter a int "))
     if not intVar:
        continue
     getReadyForSendingInt()
     sendInt(intVar)

     
     #send float to arduino
     var = float(input("Enter a float number "))
     if not var:
         continue
     getReadyForSendingFloat()
     sentFloat(var)
     
     
     # sleep one second
     time.sleep(1)
     
     number = bus.read_byte(address)
     #if its ascii is 35, we are going to read a float(4 bytes)
     if number == FloatHeader:
        result = readFloat()
        print("I received a float",result)
        
     print()


if __name__ == '__main__':
   try:
      communicate()
   except Exception as e:
      print("error message: " + str(e))
      print("end")
