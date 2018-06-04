#include "LSM9DS1_c_wrapper.h"
#include "LSM9DS1.h"

LSM9DS1* lsm9ds1_create() {
    return new LSM9DS1(IMU_MODE_I2C, 0x6b, 0x1e);
}

void lsm9ds1_begin(LSM9DS1* obj) {
    obj->begin();
}

void lsm9ds1_calibrate(LSM9DS1* obj) {
    obj->calibrate();
}

int lsm9ds1_gyroAvailable(LSM9DS1* obj) {
    return obj->gyroAvailable();
}

int lsm9ds1_accelAvailable(LSM9DS1* obj) {
    return obj->accelAvailable();
}

int lsm9ds1_magAvailable(LSM9DS1* obj) {
    return obj->magAvailable();
}

void lsm9ds1_readGyro(LSM9DS1* obj) {
    obj->readGyro();
}

void lsm9ds1_readAccel(LSM9DS1* obj) {
    obj->readAccel();
}

void lsm9ds1_readMag(LSM9DS1* obj) {
    obj->readMag();
}

float lsm9ds1_getGyroX(LSM9DS1* obj) {
    return obj->gx;
}
float lsm9ds1_getGyroY(LSM9DS1* obj) {
    return obj->gy;
}
float lsm9ds1_getGyroZ(LSM9DS1* obj) {
    return obj->gz;
}

float lsm9ds1_getAccelX(LSM9DS1* obj) {
    return obj->ax;
}
float lsm9ds1_getAccelY(LSM9DS1* obj) {
    return obj->ay;
}
float lsm9ds1_getAccelZ(LSM9DS1* obj) {
    return obj->az;
}

float lsm9ds1_getMagX(LSM9DS1* obj) {
    return obj->mx;
}
float lsm9ds1_getMagY(LSM9DS1* obj) {
    return obj->my;
}
float lsm9ds1_getMagZ(LSM9DS1* obj) {
    return obj->mz;
}

float lsm9ds1_calcGyro(LSM9DS1* obj, float gyro) {
    return obj->calcGyro(gyro);
}
float lsm9ds1_calcAccel(LSM9DS1* obj, float accel) {
    return obj->calcAccel(accel);
}
float lsm9ds1_calcMag(LSM9DS1* obj, float mag) {
    return obj->calcMag(mag);
}