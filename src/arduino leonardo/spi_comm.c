//
//  spi.c
//  
//
//  Created by Matt Kollada on 5/20/17.
//
//

#include "ddefs.h"
#include "dshare.h"
#include "Arduino.h"
//#include <SPI.h>

uint8_t pwm;
uint8_t servoAngle;
uint8_t marker;
uint8_t dat;
uint8_t receive;

uint8_t tmp;

void spiHandler()
{ 
  switch (marker)
  {
  case 0:
    dat = SPDR;
    receive = dat;
//    Serial.println(dat);
//    Serial.print(dat);
    if (dat == 1)
    {
      SPDR = 3;
      marker++;
//      Serial.print("received: ");
//      Serial.println(dat);
      break;
    }
    else if (dat == 2) {
      SPDR = 4;
      marker++; 
//      Serial.print("received: ");
//      Serial.println(dat);
      break;
    }
    else if (dat == 3) {
      SPDR = 5;
      marker++;
      break;
    }
    else if (dat == 4) {
      servoAngle = 90;
      break;
    }
    else {
//      Serial.print("error1: ");
//      Serial.println(dat);
    }
    break;    
  case 1:
    tmp = SPDR;
    if(tmp == 1 || tmp == 2 || tmp == 3 || tmp == 4) {
      break;
    }
    if(receive == 1) {
      pwm = tmp;
      SPDR = 6;
      setData( BLDC_DUTY_CYCLE ,pwm );
//      Serial.print("pwm: ");
//      Serial.println(pwm);
      marker = 0;
      break;
    }
    else if (receive == 2) {
      servoAngle = tmp;
      SPDR = 7;
      setData( SERVO_ANGLE ,servoAngle );
//      Serial.print("servo: ");
//      Serial.println(servoAngle);
      marker = 0;
      break;
    }
    else if (receive == 3) {
      pwm = tmp;
      SPDR = 8;
      setData( BLDC_DUTY_CYCLE , -pwm );
      marker = 0;
      break;
    }
    else {
//      Serial.print("error2: ");
//      Serial.println(dat); 
    }
    receive = 0;
    break;
  }
}
