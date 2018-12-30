  /*
 * Code modified from WASD.ino from PiCar Mobile Movement Control Project
 * Authors: Hayden Sierra and Daniel Kelly
 *
 * Modified code included PID controller code for motor 
 * Author: AnZou(anzou@wustl.edu)
 * PID speed control for BLCD
 * BLDC(+ESC): TRACKSTAR
 * Encoder: YUMOE6A2
 * Controller: Arduino UNO R3
*/

/*
 * Pin Definition
 * Pin2 for encoder: interrupt signal
 * Pin13 for BLDC ESC: PPM signal
 * 
*/

#include <Servo.h>
Servo myservo;

//Steering controls
int controlNumber = 0;
double control_signal = 100;
boolean from_left = false;

//Global variables
double encoder_counter;
double motor_speed; //RPS

//Proportional moter speed controller variables
const double REFERENCE_SIGNAL = 12; //Set the speed in RPS
const double K_p=0.1;
double e_k = 0;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);
  myservo.attach(9);

  pinMode(13, OUTPUT);
  delay(3000);
}

void loop() {
  //Read command from Raspberry Pi
  while (Serial.available() > 0) {
    controlNumber = Serial.read() - 48;
  }
  
  //Take action directed by Raspberry Pi
  switch(controlNumber){
    case 1 :
      //Go forward, wheels straight
      if(from_left == true){
        from_left = false;
        myservo.write(75);
        delay(100);
      }
      myservo.write(95);
      control_signal = control_signal + controller_increment();
      PPM_output(control_signal);
      break;
    case 2 :
      //Go forward, wheels pointing 15 degrees left
      from_left = true;
      myservo.write(110);
      control_signal = control_signal + controller_increment();
      PPM_output(control_signal);
      break;
    case 3 :
      //Go forward, wheels pointing 15 degrees right
      if(from_left == true){
        from_left = false;
        myservo.write(75);
        delay(100);
      }
      myservo.write(80);
      control_signal = control_signal + controller_increment();
      PPM_output(control_signal);
      break;
    case 4 :
      //Stop and point wheels straight
      PPM_output(0);
      if(from_left == true){
        from_left = false;
        myservo.write(75);
        delay(100);
      }
      myservo.write(95);
      break;
    default :
      PPM_output(0); 
  }
}

//Output to motor
void PPM_output(int command) {
  int rate = 1500 + command;
  digitalWrite(13, HIGH);
  delayMicroseconds(rate);
  digitalWrite(13, LOW);
  delayMicroseconds(10000);
  delayMicroseconds(10000 - rate);
}

void speed_measure() {
  // measures the motor rpm using quadrature encoder
  encoder_counter = 0;
  attachInterrupt(0, encoder, RISING);
  delay(50); // Wait for 50 ms
  detachInterrupt(0);
  motor_speed =  encoder_counter * 20 / 200;
}

void encoder()
{  
  // increments the encoder count when a rising edge
  // is detected by the interrupts  
  encoder_counter = encoder_counter + 1;
}

double controller_increment()
{
  double increment;
  speed_measure();
  e_k = REFERENCE_SIGNAL - motor_speed;
  
  if((e_k>0)||(e_k<0))
  {
    increment = K_p*e_k;
  }
  else
  {
    increment = 0;  
  }
  
  //increment boundary/saturation
  if(increment > 1)
  {
   increment = 1; 
  }
  
  if(increment < -1)
  {
   increment = -1; 
  }
  
  return increment;
}
