#ifndef DDEF_H_
#define DDEF_H_

// length of the internal storage array
#define ARR_LENGTH 32

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

// etc...

#endif
