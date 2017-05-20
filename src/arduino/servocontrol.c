//
//  servocontrol.c
//
//
//  Created by Matt Kollada on 5/17/17.
//
//

#include "servocontrol.h"
#include <Servo.h>

Servo servo;

void attachServoToPin() {
  servo.attach( SERVO_PIN );
}

void setServoAngle(int8_t angle) {
  if( angle > 0 & angle <180) {
    servo.write(angle);
  }
}

