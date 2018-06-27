#ifndef DDEF_H_
#define DDEF_H_

// length of the internal storage array
#define DSHARE_ARR_LENGTH 32

/*************************
  Error Codes
*************************/
#define DSHARE_OK        0
#define DSHARE_INVALID   1
#define DSHARE_NOUPDATE  2


/*************************
  Addresses
*************************/
// IMU
#define IMU_ACCEL_X      0 // see figure in page 10 of LSM9DS1 datasheet
#define IMU_ACCEL_Y      1
#define IMU_ACCEL_Z      2
#define IMU_GYRO_ZY      3
#define IMU_GYRO_XZ      4
#define IMU_GYRO_YX      5
#define IMU_MAGNET_X     6
#define IMU_MAGNET_Y     7
#define IMU_MAGNET_Z     8
#define IMU_TEMP         9
#define IMU_FILTER_A     10 // low pass filter parameters
#define IMU_FILTER_B     11

// Control Params
#define SPEED_PID_P      12
#define SPEED_PID_I      13
#define SPEED_PID_D      14
#define SPEED_PID_DFILT  15

// BLDC
#define BLDC_DUTY_CYCLE  16
#define BLDC_HALL_SPEED  17
#define DIRECTION        18

// Servo
#define SERVO_ANGLE      19

// Max Speed/Angle
#define MAX_SPEED        20
#define MAX_SERVO_ANGLE  21

// Current sensing from motor drivers
#define CURRENT_ONE      22
#define CURRENT_TWO      23
#define CURRENT_THREE    24

// Kill Switch
#define KILL_SWITCH      25


#endif
