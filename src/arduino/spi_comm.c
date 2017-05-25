//
//  spi.c
//  
//
//  Created by Matt Kollada on 5/20/17.
//
//

#include "ddefs.h"
#include "dshare.h"
#include <Arduino.h>

int pwm;
int servoAngle;
int marker;
unsigned char dat;
byte receive;

void spiHandler()
{
  switch (marker)
  {
  case 0:
//    Serial.print(receive);
    dat = SPDR;
    receive = dat;
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
    break;    
  case 1:
    if(receive == 1) {
      pwm = SPDR;
      SPDR = pwm;
      setData( BLDC_DUTY_CYCLE ,pwm );
//      Serial.print("pwm: ");
//      Serial.println(pwm);
      marker = 0;
    }
    else if (receive == 2) {
      servoAngle = SPDR;
      SPDR = servoAngle;
      setData( SERVO_ANGLE ,pwm );
//      Serial.print(servoAngle);
//      Serial.print("servo: ");
      marker = 0;
    }
    else {
//      Serial.println("dat is wrong 2"); 
    }
    break;
  }
}

