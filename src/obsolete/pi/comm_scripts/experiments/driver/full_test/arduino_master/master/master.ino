#include <Servo.h>

Servo steer;
Servo esc;

const int escIn = 5;// 8;
const int steerIn = 6;//9;

const int steerOut = 10;//3;
const int escOut = 9;//5;

void setup(){
  Serial.begin(9600);
  
  pinMode(escIn, INPUT);
  pinMode(steerIn, INPUT);
  
  pinMode(steerOut, OUTPUT);
  pinMode(escOut, OUTPUT);
  
  steer.attach(steerOut);
  esc.attach(escOut);
  //steer.writeMicroseconds(1500);
  //esc.writeMicroseconds(1500);
  delay(5);
}

void loop(){
  int escCommand = map(pulseIn(escIn, HIGH), 1901, 959, 1000, 2000);
  int steerCommand = map(pulseIn(steerIn, HIGH), 1220, 1490, 1000, 2000);
  esc.writeMicroseconds(escCommand);
  steer.writeMicroseconds(steerCommand);
  Serial.print(escCommand);
  Serial.print(".");
  Serial.println(steerCommand);
  delay(30);
}
