//
//  servocontrol.h
//
//
//  Created by Matt Kollada on 5/17/17.
//
//

#ifndef SERVOCONTROL_H_
#define SERVOCONTROL_H_

#include <stdint.h>
#include "ddefs.h"

#ifdef __cplusplus
extern "C" {
#endif

#define SERVO_PIN 5

//#include <Servo.h>

void attachServoToPin();
void setServoAngle( int16_t );

#ifdef __cplusplus
}
#endif


#endif

