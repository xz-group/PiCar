#include <Wire.h>
#define SLAVE_ADDRESS 0x04

byte inputByte = 0;
int currentFloatByte = 1;
int beginSendingFloat = 0;
float data = 3.14159;

int beginReadingFloat = 0;
int currentReadingFloatByte = 1;

typedef union{
byte asBytes[4];
float asFloat;
} floatval;

floatval v;

int intHeader = 36;
int beginReadingInt = 0;
int intData = 0;


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
      readFloatByByte();
    }
    else if(beginReadingInt){
      readInt();
    }
    else{
      inputByte = Wire.read();
      if(inputByte == 35 && !beginReadingFloat){
        beginReadingFloat = 1;
      }
      else if(inputByte == 36 && !beginReadingInt){
        beginReadingInt = 1;
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
  else
  {
    sendFloatByByte(); 
  }    
}

void readInt(){
  intData = Wire.read();
  Serial.print("The int we received is:");
  Serial.println(intData);
  beginReadingInt = 0;
}

void readFloatByByte(){
  switch(currentReadingFloatByte){
      case 1:
      v.asBytes[0] = Wire.read();
      currentReadingFloatByte = 2;
      break;
      
      case 2:
      v.asBytes[1] = Wire.read();
      currentReadingFloatByte = 3;
      break;
      
      case 3:
      v.asBytes[2] = Wire.read();
      currentReadingFloatByte = 4;
      break;
      
      case 4:
      currentReadingFloatByte = 1;
      v.asBytes[3] = Wire.read();
      beginReadingFloat = 0;
      
      Serial.print("The float we received is:");
      Serial.println(v.asFloat,5);
      break;
    }
}

void sendFloatByByte(){
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
