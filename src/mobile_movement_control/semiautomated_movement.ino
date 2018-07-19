/*
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

#define reference_signal 35 // set the speed in RPS here
#include <Servo.h>
#define K_p 0.1
#define K_i 0
#define K_d 0.001
#include <Wire.h>
#define SLAVE_ADDRESS 0x04
#define KILL_SWITCH_IN 1 //using interrupt 1 for kill switch
#define KILL_SWITCH_IN_PIN 3 //interrupt 1 = digital pin 3
#define KILL_SWITCH_OUT_PIN 7

unsigned long t = 0;
double encoder_counter;
double motor_speed; //rotations per second
int number = 0;
double control_signal;
double e_k; // variable for P
double e_k1; // variable for I (not in use)
double e_k2; // variable for D (not in use)
Servo myservo;
int servo_angle = 90;
int state = 0;
int times = 0;
int flag = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  myservo.attach(9);
  e_k = 0;
  e_k1 = 0;
  e_k2 = 0; 
  control_signal = 150; //PWM

  attachInterrupt(KILL_SWITCH_IN, kill, RISING); //for kill switch
  pinMode(KILL_SWITCH_OUT_PIN, OUTPUT);
  digitalWrite(KILL_SWITCH_OUT_PIN, HIGH);
  Serial.println("Start!");
  pinMode(13, OUTPUT);
  delay(3000);

  Serial.println("Calibrating ESC for positive RPM");
  calibration(500); // Calibrating ESC for +ve RPM
  Serial.println("Calibrating ESC for negative RPM");
  calibration(-500); // Calibrating ESC for -ve RPM
  Serial.println("Calibrating ESC for zero RPM");
  calibration(0); // Calibrating ESC for 0 RPM

  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);

  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  Serial.println("Ready!");
}

void loop() {
  
  if (flag == 1){
    unsigned long currentMillis = millis();
    myservo.write(servo_angle);
    if(currentMillis - t > number*1000) {
      Serial.println("Finished");
      PPM_output(0);
    }
  
    else {
      control_signal = control_signal + increment_pid();
      PPM_output(control_signal);
      Serial.println("Running: ");
    }
  }
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

double increment_pid()
{
  double increment;
  speed_measure();
  e_k2 = e_k1;
  e_k1 = e_k;
  e_k = reference_signal - motor_speed;
  
  if((e_k>5)||(e_k<-5))
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

void PPM_output(int command) {
  int rate = 1500 + command;
  digitalWrite(13, HIGH);
  delayMicroseconds(rate);
  digitalWrite(13, LOW);
  delayMicroseconds(10000);
  delayMicroseconds(10000 - rate);
}

void receiveData(int byteCount){
  while(Wire.available()) {
    flag = 0;
    if (times == 0){
      number = Wire.read();
      Serial.print("Seconds Received: ");
      Serial.println(number);
      t = millis();
      times++;
    }
    else {
      servo_angle = Wire.read();
      if (servo_angle > 127){
        servo_angle = 127;
        Serial.print("Max Tire Angle is 127");
      }
      else if (servo_angle < 53){
        servo_angle = 53;
        Serial.print("Smallest Tire Angle is 53");
      }
      Serial.print("Tire Angle Received: ");
      Serial.println(servo_angle);
      t = millis();
      times = 0;
      flag = 1;
    }
  }
}

// callback for sending data
void sendData(){
  Wire.write(number);
}

void kill(){
  digitalWrite(KILL_SWITCH_OUT_PIN, LOW);
}
