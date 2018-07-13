#include <Servo.h>

Servo steer;
Servo esc;

int steerPin = 9;//3;
int escPin = 10;//5;

const int danger = 500;
int lastCommand = 0;

void setup(){
  Serial.begin(9600);
  pinMode(steerPin, OUTPUT);
  pinMode(escPin, OUTPUT);

  steer.attach(steerPin);
  esc.attach(escPin);
  

}

void loop(){
  if(Serial.available()){
    if(Serial.read()=='e'){
      esc.writeMicroseconds(Serial.parseInt());
    }else{
      steer.writeMicroseconds(Serial.parseInt());
    }
    lastCommand = millis();
  }else{
    if((millis()-lastCommand) > danger){
      esc.writeMicroseconds(1500);
      steer.writeMicroseconds(1500);
    }
  }
}
