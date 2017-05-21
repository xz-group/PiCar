//  Created by Matt Kollada on 5/17/17.

#include <stdint.h>
#include <Servo.h>
#include "dshare.h"
#include "ddefs.h"
#include "servocontrol.h"
#include "spi_comm.h"
#include "timers.h"

Servo servo;

int16_t angle;
int16_t pwm;

// Servo Pwm Update interrupt
ISR(TIMER0_COMPA_vect)
{
  if ( getData( SERVO_ANGLE, &angle ) == DSHARE_OK ) {
    servo.write( angle );
  }
  if ( getData( BLDC_DUTY_CYCLE, &pwm ) == DSHARE_OK ) {
      //run PID on PWM
  }
}

// SPI Interrupt (dealing with issue with SPSR)
ISR(SPI_STC_vect) {
  if ((SPSR & (1 << SPIF)) != 0)
  {
    spiHandler();
  }
}

// IMU Interrupt
ISR(TIMER3_COMPA_vect) {
  //read IMU and set global data structure
  getIMUData();
}

void setup() {
  Serial.begin(115200);
//  SPI.attachInterrupt();
  pinMode(MISO, OUTPUT);
  SPCR |= _BV(SPE);

  initTimers();
  
  setData( SERVO_ANGLE, 90 );
  servo.attach( SERVO_PIN );

  imuSetup();
  // interrupt on Compare A Match
}  // end of setup

void loop() {

}

void testIMU() {
  //  getIMUData();

//  Serial.print( "accelX: ");
//  Serial.println( dataArr[ IMU_ACCEL_X ] );
//  Serial.print( "accelY: ");
//  Serial.println( dataArr[ IMU_ACCEL_Y ] );
//  Serial.print( "accelZ: ");
//  Serial.println( dataArr[ IMU_ACCEL_Z ] );
//
//  Serial.print( "GyroX: ");
//  Serial.println( dataArr[ IMU_GYRO_ZY ] );
//  Serial.print( "GyroY: ");
//  Serial.println( dataArr[ IMU_GYRO_XZ ] );
//  Serial.print( "GyroZ: ");
//  Serial.println( dataArr[ IMU_GYRO_YX ] );
//
//  Serial.print( "MagnetX: ");
//  Serial.println( dataArr[ IMU_MAGNET_X ] );
//  Serial.print( "MagnetY: ");
//  Serial.println( dataArr[ IMU_MAGNET_Y ] );
//  Serial.print( "MagnetZ: ");
//  Serial.println( dataArr[ IMU_MAGNET_Z ] );
//
//  Serial.print("Temp: ");
//  Serial.println( dataArr[ IMU_TEMP ] );
//
//  delay(50);
}






