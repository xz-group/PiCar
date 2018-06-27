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

#define K_p 0.1
#define K_i 0
#define K_d 0.001

double encoder_counter;
double motor_speed; //rotations per second

double control_signal;
double e_k; // variable for P
double e_k1; // variable for I (not in use)
double e_k2; // variable for D (not in use)


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  e_k = 0;
  e_k1 = 0;
  e_k2 = 0;
  control_signal = 150; //PWM

  Serial.println("Start!");
  pinMode(13, OUTPUT);
  delay(3000);

  Serial.println("Calibrating ESC for positive RPM");
  calibration(500); // Calibrating ESC for +ve RPM
  Serial.println("Calibrating ESC for negative RPM");
  calibration(-500); // Calibrating ESC for -ve RPM
  Serial.println("Calibrating ESC for zero RPM");
  calibration(0); // Calibrating ESC for 0 RPM
}

void loop() {
  // put your main code here, to run repeatedly:
  control_signal = control_signal + increment_pid();
  //High and low boundary
  //Serial.println("motor speed:");
  //Serial.println(motor_speed);
  //Serial.println("output:");
  //Serial.println(control_signal);
  PPM_output(control_signal);
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
