//  Created by Matt Kollada on 5/17/17.

#include <stdint.h>
#include <Servo.h>
#include <SPI.h>
#include "dshare.h"
#include "ddefs.h"
#include "servocontrol.h"
#include "spi_comm.h"
#include "timers.h"
#include "imu.h"

Servo servo;
Servo esc;

int SPEED_SCALE = 2.5;

//uint8_t servoAngle;
//uint8_t pwm;

int tempAngle = 90;
int tempPWM = 0;


// Servo Pwm Update interrupt
ISR(TIMER0_COMPA_vect)
{
  if ( getData( SERVO_ANGLE, &tempAngle ) == DSHARE_OK ) {
      servo.write(tempAngle);
  }
  if ( getData( BLDC_DUTY_CYCLE, &tempPWM ) == DSHARE_OK ) {
      //run PID on PWM
      esc.writeMicroseconds(1500 + SPEED_SCALE*tempPWM);
  }
}

// SPI Interrupt (dealing with issue with SPSR)
ISR(SPI_STC_vect) {
    spiHandler();
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
  
  // set initial values of global data structure for servo and pwm
//  setData( SERVO_ANGLE, 90 );
//  setData( BLDC_DUTY_CYCLE, 0 );

  // setup esc and servo
  servo.attach( 3 );
  esc.attach( 5 );

  // Turn kill switch off
  setData( KILL_SWITCH, 1 );

  //setup IMU
  imuSetup();
} 

void loop() {
  Serial.println(tempAngle);
  Serial.println(1500 + SPEED_SCALE*tempPWM);
}


