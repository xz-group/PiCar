float data = 3.14159;

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
