//
//  BLDC.h
//  
//
//  Created by Matt Kollada on 5/16/17.
//
//

#ifndef BLDC_h
#define BLDC_h

//PWM
uint8_t getPWM( int16_t *pwm );
uint8_t setPWM( int16_t pwm );

//Direction
uint8_t getDirection( int16_t *direction );
uint8_t setDirection( int16_t direction );

//Motor Commutation functions
void moveForward( int16_t pwm );
void moveBackward( int16_t pwm );

//Read Speed from Hall Sensors
int16_t hallSpeed( int16_t time, int8_t[] hallVals);

#endif /* BLDC_h */
