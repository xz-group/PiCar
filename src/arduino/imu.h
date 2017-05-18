//
//  IMU.h
//  
//
//  Created by Matt Kollada on 5/16/17.
//
//

#ifndef IMU_H_
#define IMU_H_

//Acceleration
uint8_t getAccelX( int16_t *accelX );
uint8_t setAccelX( int16_t accelX );
uint8_t getAccelY( int16_t *accelY );
uint8_t setAccelY( int16_t accelY );
uint8_t getAccelZ( int16_t *accelZ );
uint8_t setAccelZ( int16_t accelZ );

//Gyroscope
uint8_t getGyroX( int16_t *gyroX );
uint8_t setGyroX( int16_t gyroX );
uint8_t getGyroY( int16_t *gyroY );
uint8_t setGyroY( int16_t gyroY );
uint8_t getGyroZ( int16_t *gyroZ );
uint8_t setGyroZ( int16_t gyroZ );

//Magnet
uint8_t getMagnetX( int16_t *magnetX );
uint8_t setMagnetX( int16_t magnetX );
uint8_t getMagnetY( int16_t *magnetY );
uint8_t setMagnetY( int16_t magnetY );
uint8_t getMagnetZ( int16_t *magnetZ );
uint8_t setMagnetZ( int16_t magnetZ );

//Temp
uint8_t getTemp( int16_t *temp );
uint8_t setTemp( int16_t *temp );

//Filter
uint8_t getFilterA( int16_t filterA );
uint8_t setFilterA( int16_t filterA );
uint8_t getFilterB( int16_t filterB );
uint8_t setFilterB( int16_t filterB );

//ISR
ISR( ) // timer interrupt

#endif /* IMU_h */
