#include <stdint.h>

#ifndef DDEF_H_
#define DDEF_H_

// length of the internal storage array
#define DSHARE_ARR_LENGTH 32

/*************************
* Error Codes            *
*************************/
#define DSHARE_OK        0
#define DSHARE_INVALID   1
#define DSHARE_NOUPDATE  2


/*************************
* Addresses              *
*************************/
// IMU
#define IMU_ACCEL_X      (uint8_t) 0 // see figure in page 10 of LSM9DS1 datasheet
#define IMU_ACCEL_Y      (uint8_t) 1
#define IMU_ACCEL_Z      (uint8_t) 2
#define IMU_GYRO_ZY      (uint8_t) 3
#define IMU_GYRO_XZ      (uint8_t) 4
#define IMU_GYRO_YX      (uint8_t) 5
#define IMU_MAGNET_X     (uint8_t) 6
#define IMU_MAGNET_Y     (uint8_t) 7
#define IMU_MAGNET_Z     (uint8_t) 8
#define IMU_TEMP         (uint8_t) 9
#define IMU_FILTER_A     (uint8_t) 10 // low pass filter parameters
#define IMU_FILTER_B     (uint8_t) 11

// Control Params
#define SPEED_PID_P      (uint8_t) 12
#define SPEED_PID_I      (uint8_t) 13
#define SPEED_PID_D      (uint8_t) 14
#define SPEED_PID_DFILT  (uint8_t) 15

// BLDC
#define BLDC_DUTY_CYCLE  (uint8_t) 16
#define BLDC_HALL_SPEED  (uint8_t) 17
#define DIRECTION        (uint8_t) 18

// Servo
#define SERVO_ANGLE      (uint8_t) 19


#endif
