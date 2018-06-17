import smbus
import time
import struct

# for RPI version 1, use  ^ ^ bus = smbus.SMBus(0) ^ ^
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

temperatura = 10.2
vazao = 5.3
command = 20
teste = 30


def readFloat():
   print("in readFlaot")
   byte1 = bus.read_byte(address)
   print("Byte 1 is: ",byte1)
   byte2 = bus.read_byte(address)
   print("Byte 2 is: ",byte2)
   byte3 = bus.read_byte(address)
   print("Byte 3 is: ",byte3)
   byte4 = bus.read_byte(address)
   print("Byte 4 is: ",byte4)

   #convert the binary to float
   result = struct.unpack('f', bytes([byte4,byte3,byte2,byte1]))

   time.sleep(0.5)
   return result


def sentFloat(data):
    binary = struct.pack('f',data)
    for byte in binary:
        print("I sent arduino:",byte)
        bus.write_byte(address,byte)


def communicate():
   while True:
     var = 35
     bus.write_byte(address,var)
     print("RPI: Hi Arduino, I sent you ", chr(var))
     sentFloat(1.929234)

     # sleep one second
     time.sleep(1)


     #Uncomment following part and comment the above part
     #if you are trying to read float from arduino
     
     #var = 35
     #bus.write_byte(address,var)
     #print("RPI: Hi Arduino, I sent you ", chr(var))
     #number = bus.read_byte(address)
     #if its ascii is 35, we are going to read a float(4 bytes)
     #if number == 35:
     #   result = readFloat()
     #   print("The float is:",result)

     #print("RPI: I received a digit ", number)
     print()


if __name__ == '__main__':
   try:
      communicate()
   except Exception as e:
      print("error message: " + str(e))
      print("end")
