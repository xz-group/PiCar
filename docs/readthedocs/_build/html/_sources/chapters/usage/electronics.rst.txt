Electronics
=============


Pi and Arduino Communication
----------------------------

I2C Method
^^^^^^^^^^

*The code is from https://oscarliang.com/raspberry-pi-arduino-connected-i2c/, with slight changes to accommodate python 3 instead of python 2*

Using I2C protocol, we could communicate between raspberry pi and arduino using only three wires

The wiring is:

.. image:: electronics/PiArduinoI2CHardware_bb.jpg
  :width: 500

Raspberry pi and Arduino both agree on the a slave address of 0x04

**Upload Arduino code to Arduino board**

The testing code is:

.. code-block:: c
  :linenos:

  #include <Wire.h>
  #define SLAVE_ADDRESS 0x04
  int number = 0;
  int state = 0;

  void setup() {
    pinMode(13, OUTPUT);
    Serial.begin(9600); // start serial for output

    // initialize i2c as slave
    Wire.begin(SLAVE_ADDRESS);

    // define callbacks for i2c communication
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
    Serial.println("Ready!");
  }

  void loop() {
    delay(100);
  }

  // callback for received data
  void receiveData(int byteCount){
    while(Wire.available()) {
      number = Wire.read();
      Serial.print("data received: ");
      Serial.println(number);
      if (number == 1){
        if (state == 0){
          digitalWrite(13, HIGH); // set the LED on
          state = 1;
        }
        else{
          digitalWrite(13, LOW); // set the LED off
          state = 0;
        }
      }
    }
  }

  // callback for sending data
  void sendData(){
    Wire.write(number);
  }

**Run the python code on the raspberry pi**

The testing code is:

.. code-block:: python
  :linenos:

  import smbus
  import time
  # for RPI version 1, use  ^ ^ bus = smbus.SMBus(0) ^ ^
  bus = smbus.SMBus(1)

  # This is the address we setup in the Arduino Program
  address = 0x04

  def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value)
    return -1

  def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number

  while True:
    var = int(input("Enter 1  ^ ^  9: "))
    if not var:
        continue

    writeNumber(var)
    print("RPI: Hi Arduino, I sent you ", var)
    # sleep one second
    time.sleep(1)

    number = readNumber()
    print("Arduino: Hey RPI, I received a digit ", number)
    print()

See Also:
#########
* `SMBus Package <https://pypi.org/project/smbus-cffi/>`_



SPI Method
^^^^^^^^^^


USB Method
^^^^^^^^^^


Resources
^^^^^^^^^
* `I2C <https://learn.sparkfun.com/tutorials/i2c>`_

I2C SPI Reference page

Contributors: Jerry Kong, Shadi Davari, Josh Jin
