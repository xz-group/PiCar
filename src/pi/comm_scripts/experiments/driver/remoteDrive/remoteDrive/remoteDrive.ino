/*
 * Script to drive the Pi Car using the remote control.
 * The Arduino reads in pulse width value from the receiver
 * then maps it appropriately and sends it to either 
 * the ESC or the steering servo.
 */
 
 #include <Servo.h>
 
 Servo steer;
 Servo esc;
 
 const int steerPin = 3;
 const int escPin = 5;
 
 const int steerIn = 9;
 const int escIn = 8;
 
 void setup(){
   pinMode(steerPin, OUTPUT);
   pinMode(escPin, OUTPUT);
   
   pinMode(steerIn, INPUT);
   pinMode(escIn, INPUT);
   
   steer.attach(steerPin);
   esc.attach(escPin);
 }
 
 void loop(){
   steer.writeMicroseconds(map((int)((int)pulseIn(steerIn, HIGH)/50)*50, 1220, 1490, 1000, 2000));
   esc.writeMicroseconds(map(pulseIn(escIn, HIGH), 
         1901, 959, 1000, 2000)); // Values found from test script
 }
