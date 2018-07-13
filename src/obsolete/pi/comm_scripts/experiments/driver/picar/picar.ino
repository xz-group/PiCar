/*
 * Script to communicate with the Pi Car through the Arduino.
 * Uses Serial as the interface at 9600 baud.
 * 
 * Send 's' to put in the steering state. Then a steering
 * value can be sent. 
 *
 * Send 'e' to put in the ESC state. Then an ESC value can be
 * sent.
 *
 * When sending numbers, prepend them with any (non 's' or 'e')
 * char to notify the program that you're sending a number. This
 * character will be discarded.
 */

#include <Servo.h>

enum State{
  recvSteering,
  recvEsc
};
State state = recvSteering;

Servo steer;
Servo esc;

int steerPin = 3;
int escPin = 5;

int readInt();

void setup(){
  Serial.begin(9600);
  pinMode(steerPin, OUTPUT);
  pinMode(escPin, OUTPUT);

  steer.attach(steerPin);
  esc.attach(escPin);

  // Calibrate the esc
  esc.writeMicroseconds(2000);
  delay(3000);
  esc.writeMicroseconds(1000);
  delay(3000);
  esc.writeMicroseconds(1500);
}

void loop(){
  if(Serial.available()){
    switch((char)Serial.read()){
    case 's': 
      state = recvSteering;
      Serial.println("State s");
      break;
    case 'e': 
      state = recvEsc;
      Serial.println("State e");
      break;
    default: 
      switch(state){
        int x;
      case recvSteering: 
        x = Serial.parseInt();
        steer.write(x);
        Serial.println(x);
        break;
      case recvEsc: 
        x = Serial.parseInt();
        esc.writeMicroseconds(x);
        Serial.println(x);
        break;
      default: 
        break;
      }
    } 
  }
}

