/*
Author: Feiyang Jin
Email: feiyang.jin@wustl.edu
Organization: Washington University in St. Louis
Date: July 2018
*/
float data = 3.14159;

//This union is where we save the float
//Union saves all data in same address
//So the structure looks like:
//byte1-byte2-byte3-byte4
//F----L----O----T---E
//Basically the byte array and float share same data at one address
typedef union{
byte asBytes[4];
float asFloat;
} floatval;

floatval v;


void setup(){
Serial.begin(9600);

}

void loop(){

  if(Serial.available() > 0){

    byte header = Serial.read();
    if(header == 35){
      while(!(Serial.available() > 3))
      { continue;}
      for(int i=0;i<4;i++){
        v.asBytes[i] = Serial.read();
      }

      data = v.asFloat;
      sendFloat();
    }

  }

}

void sendFloat(){
  volatile unsigned long rawBits;
  rawBits =  *(unsigned long *) &data;
  //first write float header
  Serial.write("#");
  Serial.write(rawBits >> 24 & 0xff);
  Serial.write(rawBits >> 16 & 0xff);
  Serial.write(rawBits >> 8 & 0xff);
  Serial.write(rawBits & 0xff);
}
