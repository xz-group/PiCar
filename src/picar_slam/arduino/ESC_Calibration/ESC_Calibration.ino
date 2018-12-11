/*
 * Code taken from WASD.ino from PiCar Mobile Movement Control Project
 * Authors: Hayden Sierra and Daniel Kelly
 *
 * Code included PID controller code for motor 
 * Author: AnZou(anzou@wustl.edu)
 * PID speed control for BLCD
 * BLDC(+ESC): TRACKSTAR
 * Encoder: YUMOE6A2
 * Controller: Arduino UNO R3
*/

void setup() {
  pinMode(13, OUTPUT);
  delay(3000);
  
  calibration(500); // Calibrating ESC for max positive RPM
  calibration(-500); // Calibrating ESC for max negative RPM
  calibration(0); // Calibrating ESC for 0 RPM
}

void loop() {
  // No loop code
}

void calibration(int command)
{
  int i = 400;  
  while(i>1)
  {
    int rate = 1500 + command;
    digitalWrite(13, HIGH);
    delayMicroseconds(rate);
    digitalWrite(13, LOW);
    delayMicroseconds(10000);
    delayMicroseconds(10000 - rate);
    i = i-1;
  }  
}
