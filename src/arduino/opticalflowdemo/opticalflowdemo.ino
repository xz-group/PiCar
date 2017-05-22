#include <Servo.h>
#include <SPI.h>

#define SERVO_PIN 5
#define PWM_PIN 6

int pwm;
int servoAngle;

Servo servo;

ISR(SPI_STC_vect) {
  if ((SPSR & (1 << SPIF)) != 0)
  {
    spiHandler();
  }
}

void setup() {
  // put your setup code here, to run once:
  servo.attach(SERVO_PIN);
  SPI.attachInterrupt();

  pwm = 0;
  servoAngle = 90;
  
}

void loop() {
  // put your main code here, to run repeatedly:

}

//SPI transmission code
unsigned char receiveBuffer[5];
unsigned char dat;
int marker = 0;

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

///***************************************************************
//  executeCommand
//   When the complete 5 byte command sequence has been received
//   reconstitute the byte variables from the receiveBuffer
//   into integers, parse the command (add or subtract) and perform
//   the indicated operation - the result will be in resultBuffer
//****************************************************************/

void executeCommand(void)
{
    
    p1Buffer.p1Char[0] = receiveBuffer[1];
    p1Buffer.p1Char[1] = receiveBuffer[2];
    p2Buffer.p2Char[0] = receiveBuffer[3];
    p2Buffer.p2Char[1] = receiveBuffer[4];
    
    if (receiveBuffer[0] == 'a')
    {
        pwm = p1Buffer.p1Int;
        servoAngle = p2Buffer.p2Int;
        
    }
    else if (receiveBuffer[0] == 's')
    {
        resultBuffer.resultInt = p1Buffer.p1Int - p2Buffer.p2Int;
    }
    
}
