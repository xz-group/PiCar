#ifndef __SparkFunLSM9DS1_C_WRAPPER_H__
#define __SparkFunLSM9DS1_C_WRAPPER_H__

#include "LSM9DS1.h"

extern "C" {
    LSM9DS1* lsm9ds1_create();
    void lsm9ds1_begin(LSM9DS1* obj);
    void lsm9ds1_calibrate(LSM9DS1* obj);
    // Chack imu
    int lsm9ds1_gyroAvailable(LSM9DS1* obj);
    int lsm9ds1_accelAvailable(LSM9DS1* obj);
    int lsm9ds1_magAvailable(LSM9DS1* obj);
    // Read data
    void lsm9ds1_readGyro(LSM9DS1* obj);
    void lsm9ds1_readAccel(LSM9DS1* obj);
    void lsm9ds1_readMag(LSM9DS1* obj);
    // Get data
    float lsm9ds1_getGyroX(LSM9DS1* obj);
    float lsm9ds1_getGyroY(LSM9DS1* obj);
    float lsm9ds1_getGyroZ(LSM9DS1* obj);
    float lsm9ds1_getAccelX(LSM9DS1* obj);
    float lsm9ds1_getAccelY(LSM9DS1* obj);
    float lsm9ds1_getAccelZ(LSM9DS1* obj);
    float lsm9ds1_getMagX(LSM9DS1* obj);
    float lsm9ds1_getMagY(LSM9DS1* obj);
    float lsm9ds1_getMagZ(LSM9DS1* obj);
    // Compute data
    float lsm9ds1_calcGyro(LSM9DS1* obj, float gyro);
    float lsm9ds1_calcAccel(LSM9DS1* obj, float accel);
    float lsm9ds1_calcMag(LSM9DS1* obj, float mag);
}

#endif /* __SparkFunLSM9DS1_C_WRAPPER_H__ */