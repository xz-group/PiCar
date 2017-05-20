//
//  servocontrol.h
//
//
//  Created by Matt Kollada on 5/17/17.
//
//

#ifndef SERVOCONTROL_H_
#define SERVOCONTROL_H_

#include <stdio.h>


#ifdef __cplusplus
extern "C" {
#endif

#define SERVO_PIN 5

void attachServoToPin();
void setServoAngle( int8_t );

#ifdef __cplusplus
}
#endif

#endif /* servocontrol_h */

