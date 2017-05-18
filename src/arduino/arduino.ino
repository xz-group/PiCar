//  Created by Matt Kollada on 5/17/17.
//
//

#include <stdint.h>
#include <Servo.h>
#include "dshare.h"
#include "ddefs.h"

#define SERVO_PIN 5

Servo servo;

unsigned char receiveBuffer[5];
unsigned char dat;
byte marker = 0;

int16_t angle;
int16_t pwm;

/*************************************************************
 Unions allow variables to occupy the same memory space a 
 convenient way to move back and forth between 8-bit and 
 16-bit values etc.  Here three unions are declared: 
 two for parameters that are passed in commands to the Arduino 
 and one to receive  the results 
 ***************************************************************/

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


ISR(TIMER0_COMPA_vect)
{   
    if( getData( SERVO_ANGLE, &angle ) == DSHARE_OK ) {
      servo.write( angle );
    }
    if( getData( BLDC_DUTY_CYCLE, &pwm ) == DSHARE_OK ) {
      
    }
}

void setup() {
    Serial.begin(115200);
    digitalWrite(10,LOW);
    SPCR |= _BV(SPE);
    // set up Timer 0
    TCCR0A = 0;          // normal operation
    TCCR0B = bit(WGM12) | bit(CS10) | bit (CS12);   // pre-scaling
    OCR0A =  999;       // compare A register value (1000 * clock speed)
    TIMSK0 = bit (OCIE1A);
    setData( SERVO_ANGLE, 90 );
    servo.attach( SERVO_PIN );
    // interrupt on Compare A Match
}  // end of setup

void loop() {

  if((SPSR & (1 << SPIF)) != 0) {
    spiHandler();
   }
  
}

/***************************************************************  
 spiHandler
   Uses the marker variable to keep track current position in the
   incoming data packet and execute accordingly
   0   - wait for to receive start byte - once received send
         the acknowledge byte
   1   - the command to add or subtract
   2-5 - two integer parameters to be added or subtracted
       - when the last byte (5) is received, call the
         executeCommand function and load the first byte of the
         result into SPDR
   6   - transmit the first byte of the result and load the 
         second byte into SPDR
   7   - transmit the second byte of of the result and reset
         the marker   
****************************************************************/


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
    receiveBuffer[marker-1] = SPDR;
    marker++;
    break;
  case 2:
    receiveBuffer[marker-1] = SPDR;
    marker++;
    break;
  case 3:
    receiveBuffer[marker-1] = SPDR;
    marker++;
    break;
  case 4:
    receiveBuffer[marker-1] = SPDR;
    marker++;
    break;
  case 5:
    receiveBuffer[marker-1] = SPDR;
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
    marker=0;
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

 p1Buffer.p1Char[0]=receiveBuffer[1];
 p1Buffer.p1Char[1]=receiveBuffer[2];
 p2Buffer.p2Char[0]=receiveBuffer[3];
 p2Buffer.p2Char[1]=receiveBuffer[4];
 
 if(receiveBuffer[0] == 'a')
 {
   setData( SERVO_ANGLE, p1Buffer.p1Int);
   setData( BLDC_DUTY_CYCLE, p2Buffer.p2Int );
   Serial.print("p1 Int ");
   Serial.println( p1Buffer.p1Int);
   Serial.print("p2 Int ");
   Serial.println( p2Buffer.p2Int);
 }
 else if (receiveBuffer[0] == 's')
 {
  resultBuffer.resultInt = p1Buffer.p1Int - p2Buffer.p2Int;
 }

}
