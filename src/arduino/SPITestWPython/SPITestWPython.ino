#include <Servo.h>
#include <SPI.h>

Servo servo;
Servo esc;

int pwm;
int servoAngle;
byte marker;
unsigned char dat;
byte receive;

unsigned long time1;

bool kill = true;
int switchVal = 1500;

#define KILL_SWITCH A0

//ISR(SPI_STC_vect) {
//  switchVal = pulseIn(KILL_SWITCH, HIGH);
//}

void setup() {
  // put your setup code here, to run once:
    //  SPI.begin();
  SPCR |= _BV(SPE);
  Serial.begin(115200);
  pinMode(MISO, OUTPUT);
//  pinMode(KILL_SWITCH, INPUT);
//  SPI.attachInterrupt();
  
  servo.attach(3);
  esc.attach(5);
  servo.write(90);
  
//  while(millis() < 6000) {
//    esc.writeMicroseconds(2000);
//    Serial.println("high");
//  }
//  while(millis() < 12000) {
//    esc.writeMicroseconds(1000);
//    Serial.println("low");
//  }
//  while(millis() < 18000) {
//    esc.writeMicroseconds(1500);
//    Serial.println("middle");
//  }
}

void loop() {
  // put your main code here, to run repeatedly:   
    if((SPSR & (1 << SPIF)) != 0)
    { 
      spiHandler();
      time1 = millis();
   }
   
   if(servoAngle < 50) {
      servoAngle = 50;
   }
   if(servoAngle > 130) {
      servoAngle = 130;
   }

//    if((time1 - millis()) > 100) {
//      pwm = 28;
//   }
  
//  if(kill) {
       esc.writeMicroseconds(pwm*50);
       servo.write(servoAngle);
//   }
//   else {
//        esc.writeMicroseconds(1500);
//        servo.write(90);
//   }
//   Serial.println(servoAngle);
}

void spiHandler()
{
  switch (marker)
  {
  case 0:
//    Serial.print(receive);
    dat = SPDR;
    receive = dat;
    Serial.println(dat);
//    Serial.print(dat);
    if (dat == 1)
    {
      SPDR = 1;
      marker++;
    }
    else if (dat == 2) {
      SPDR = 2;
      marker++; 
    }
    else {
//      Serial.println("dat is wrong 1");
    }
//    Serial.println(dat);
    break;    
  case 1:
//      Serial.println(receive);
//    Serial.println(receive + "a");
    if(receive == 1) {
      pwm = SPDR;
      SPDR = pwm;
//      Serial.print("pwm: ");
//      Serial.println(pwm);
      marker = 0;
    }
    else if (receive == 2) {
      servoAngle = SPDR;
      SPDR = servoAngle;
//      Serial.print(servoAngle);
//      Serial.print("servo: ");
//      Serial.println(servoAngle);
      marker = 0;
    }
    else {
//      Serial.println("dat is wrong 2");
      
    }
    break;
  }
}
