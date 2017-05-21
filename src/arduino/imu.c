/*****************************************************************
Hardware setup: This library supports communicating with the
LSM9DS1 over either I2C or SPI. This example demonstrates how
to use I2C. The pin-out is as follows:
  LSM9DS1 --------- Arduino
   SCL ---------- SCL (A5 on older 'Duinos')
   SDA ---------- SDA (A4 on older 'Duinos')
   VDD ------------- 3.3V
   GND ------------- GND
(CSG, CSXM, SDOG, and SDOXM should all be pulled high. 
Jumpers on the breakout board will do this for you.)

The LSM9DS1 has a maximum voltage of 3.6V. Make sure you power it
off the 3.3V rail! I2C pins are open-drain, so you'll be 
(mostly) safe connecting the LSM9DS1's SCL and SDA pins 
directly to the Arduino.

*****************************************************************/
// The SFE_LSM9DS1 library requires both Wire and SPI be
// included BEFORE including the 9DS1 library.
//#include <Wire.h>
#include "SparkFunLSM9DS1.h"
#include "imu.h"
#include "ddefs.h"
#include "dshare.h"
#include "fp.h"

//////////////////////////
// LSM9DS1 Library Init //
//////////////////////////
// Use the LSM9DS1 class to create an object. [imu] can be
// named anything, we'll refer to that throught the sketch.
LSM9DS1 imu;

///////////////////////
// Example I2C Setup //
///////////////////////
// SDO_XM and SDO_G are both pulled high, so our addresses are:
#define LSM9DS1_M 0x1E // Would be 0x1C if SDO_M is LOW
#define LSM9DS1_AG  0x6B // Would be 0x6A if SDO_AG is LOW

bool imuSetup() {
  imu.settings.device.commInterface = IMU_MODE_I2C;
  imu.settings.device.mAddress = LSM9DS1_M;
  imu.settings.device.agAddress = LSM9DS1_AG;

  return imu.begin();
}

void getIMUData() {
  if ( imu.gyroAvailable() )
  {
    // To read from the gyroscope,  first call the
    // readGyro() function. When it exits, it'll update the
    // gx, gy, and gz variables with the most current data.
    imu.readGyro();

    // calculate gyro values and set in global data structure
    setData( IMU_GYRO_ZY, imu.calcGyro(imu.ax) );
    setData( IMU_GYRO_XZ, imu.calcGyro(imu.ay) );
    setData( IMU_GYRO_YX, imu.calcGyro(imu.az) );
  }
  if ( imu.accelAvailable() )
  {
    // To read from the accelerometer, first call the
    // readAccel() function. When it exits, it'll update the
    // ax, ay, and az variables with the most current data.
    imu.readAccel();

    // calculate accel values and set in global data structure
    setData( IMU_ACCEL_X, imu.calcAccel(imu.ax) );
    setData( IMU_ACCEL_Y, imu.calcAccel(imu.ay) );
    setData( IMU_ACCEL_Z, imu.calcAccel(imu.az) );
  }
  if ( imu.magAvailable() )
  {
    // To read from the magnetometer, first call the
    // readMag() function. When it exits, it'll update the
    // mx, my, and mz variables with the most current data.
    imu.readMag();

    // calculate magnet values and set in global data structure
    setData( IMU_MAGNET_X, imu.calcGyro(imu.ax) );
    setData( IMU_MAGNET_Y, imu.calcGyro(imu.ay) );
    setData( IMU_MAGNET_Z, imu.calcGyro(imu.az) );
  }
  if ( imu.tempAvailable() ) {
    setData ( IMU_TEMP, imu.temperature );
  }


  
  
}

