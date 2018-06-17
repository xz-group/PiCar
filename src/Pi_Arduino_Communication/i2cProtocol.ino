#include <Wire.h>
#define SLAVE_ADDRESS 0x04

int currentFloatByte = 1;
int beginSendingFloat = 0;
float data = 10.5123;

int beginReadingFloat = 0;
int currentReadingFloatByte = 1;
byte byte1;
byte byte2;
byte byte3;
byte byte4;

//Use for reading floats, Union saves all variables in same address
typedef union{
byte asBytes[4];
float asFloat;
} floatval;

floatval v;

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

}

// callback for received data
void receiveData(int byteCount){
  while(Wire.available()){
    if(beginReadingFloat){
      switch(currentReadingFloatByte){
        case 1:
        byte1 = Wire.read();
        v.asBytes[0] = byte1;
        currentReadingFloatByte = 2;
        Serial.println(byte1);
        break;

        case 2:
        byte2 = Wire.read();
        v.asBytes[1] = byte2;
        currentReadingFloatByte = 3;
        Serial.println(byte2);
        break;

        case 3:
        byte3 = Wire.read();
        v.asBytes[2] = byte3;
        currentReadingFloatByte = 4;
        Serial.println(byte3);
        break;

        case 4:
        byte4 = Wire.read();
        currentReadingFloatByte = 1;
        v.asBytes[3] = byte4;
        beginReadingFloat = 0;
        Serial.println(byte4);

        Serial.println(v.asFloat,5);
        break;
      }
    }
    else{
      byte number = Wire.read();
      Serial.print("data received: ");
      Serial.println(number);
      if(number == 35){
        beginReadingFloat = 1;
      }
    }

  }
}

// callback for sending data
void sendData(){
  if(!beginSendingFloat){
     Wire.write("#");
     beginSendingFloat = 1;
  }
  else{
    volatile unsigned long rawBits;
    rawBits =  *(unsigned long *) &data;

    switch (currentFloatByte){
      case 1:
      Wire.write(rawBits >> 24 & 0xff);
      currentFloatByte ++;
      break;

      case 2:
      Wire.write(rawBits >> 16 & 0xff);
      currentFloatByte ++;
      break;

      case 3:
      Wire.write(rawBits >> 8 & 0xff);
      currentFloatByte ++;
      break;

      case 4:
      Wire.write(rawBits & 0xff);
      currentFloatByte = 1;
      beginSendingFloat = 0;
      break;

    }

  }

}
