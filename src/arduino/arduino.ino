//  Created by Matt Kollada on 5/17/17.

#include <stdint.h>
#include <Servo.h>
#include "dshare.h"
#include "ddefs.h"
#include "servocontrol.h"
#include <SPI.h>

Servo servo;

unsigned char receiveBuffer[5];
unsigned char dat;
byte marker = 0;

int16_t angle;
int16_t pwm;

union
{
  int p1Int;
  unsigned char  p1Char [2];
} p1Buffer;

union
{
  int p2Int;
  unsigned char p2Char [2];
} p2Buffer;

union
{
  int resultInt;
  unsigned char  resultChar [2];
} resultBuffer;

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
ISR(TIMER2_COMPA_vect) {
  //read IMU and set global data structure
  //getIMUData();
}

void setup() {
  Serial.begin(115200);
  SPI.attachInterrupt();
  pinMode(MISO, OUTPUT);
  SPCR |= _BV(SPE);
  // set up Timer 0
  TCCR0A = 0;          // normal operation
  TCCR0B = bit(WGM12) | bit(CS10) | bit (CS12);   // pre-scaling
  OCR0A =  999;       // compare A register value (1000 * clock speed)
  TIMSK0 = bit (OCIE1A);
  setData( SERVO_ANGLE, 90 );
  servo.attach( SERVO_PIN );

  imuSetup();
  // interrupt on Compare A Match
}  // end of setup

void loop() {

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


///***************************************************************
// spiHandler
//   Uses the marker variable to keep track current position in the
//   incoming data packet and execute accordingly
//   0   - wait for to receive start byte - once received send
//         the acknowledge byte
//   1   - the command to add or subtract
//   2-5 - two integer parameters to be added or subtracted
//       - when the last byte (5) is received, call the
//         executeCommand function and load the first byte of the
//         result into SPDR
//   6   - transmit the first byte of the result and load the
//         second byte into SPDR
//   7   - transmit the second byte of of the result and reset
//         the marker
//****************************************************************/

void spiHandler()
{
  switch (marker)
  {
    case 0:
      dat = SPDR;
      if (dat == 'c')
      {
        SPDR = 'a';
        marker++;
      }
      break;
    case 1:
      receiveBuffer[marker - 1] = SPDR;
      marker++;
      break;
    case 2:
      receiveBuffer[marker - 1] = SPDR;
      marker++;
      break;
    case 3:
      receiveBuffer[marker - 1] = SPDR;
      marker++;
      break;
    case 4:
      receiveBuffer[marker - 1] = SPDR;
      marker++;
      break;
    case 5:
      receiveBuffer[marker - 1] = SPDR;
      marker++;
      executeCommand();
      SPDR = resultBuffer.resultChar[0];
      break;
    case 6:
      marker++;
      SPDR = resultBuffer.resultChar[1];
      break;
    case 7:
      dat = SPDR;
      marker = 0;
  }

}

/***************************************************************
  executeCommand
   When the complete 5 byte command sequence has been received
   reconstitute the byte variables from the receiveBuffer
   into integers, parse the command (add or subtract) and perform
   the indicated operation - the result will be in resultBuffer
****************************************************************/


void executeCommand(void)
{

  p1Buffer.p1Char[0] = receiveBuffer[1];
  p1Buffer.p1Char[1] = receiveBuffer[2];
  p2Buffer.p2Char[0] = receiveBuffer[3];
  p2Buffer.p2Char[1] = receiveBuffer[4];

  Serial.print("p1 Int ");
  Serial.println( p1Buffer.p1Int);
  Serial.print("p2 Int ");
  Serial.println( p2Buffer.p2Int);

  if (receiveBuffer[0] == 'a')
  {
    setData( SERVO_ANGLE, p1Buffer.p1Int);
    setData( BLDC_DUTY_CYCLE, p2Buffer.p2Int );

  }
  else if (receiveBuffer[0] == 's')
  {
    resultBuffer.resultInt = p1Buffer.p1Int - p2Buffer.p2Int;
  }

}

