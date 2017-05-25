//  Created by Matt Kollada on 5/17/17.

#include <stdint.h>
#include <Servo.h>
#include <SPI.h>
#include "dshare.c"
#include "ddefs.h"
#include "servocontrol.h"
#include "spi_comm.h"
#include "timers.h"
#include "imu.h"

Servo servo;
Servo esc;

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

//// IMU Interrupt
//ISR(TIMER3_COMPA_vect) {
//  //read IMU and set global data structure
//  getIMUData();
//}

void setup() {
  //open serial port for debugging
  Serial.begin(115200);
  
  //setup SPI
  SPI.attachInterrupt();
  pinMode(MISO, OUTPUT);
  SPCR |= _BV(SPE);

  //Initialize timers
  initTimers();
  
  setData( SERVO_ANGLE, 90 );
  servo.attach( SERVO_PIN );

  //setup IMU
  imuSetup();
  // interrupt on Compare A Match
}  // end of setup

void loop() {
  testIMU();
}

void testIMU() {
    getIMUData();
}






