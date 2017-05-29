#include <Servo.h>
#include <SPI.h>

#define MAX_SPEED 300

Servo servo;
Servo esc;

bool check = false;
int test;
int pwm;
int servoAngle;
int marker;
unsigned char dat;
byte receive;
bool kill = true;

void setup() {
  // put your setup code here, to run once:
  //uncomment for debugging
  //Setup SPI
  SPCR |= _BV(SPE);
  pinMode(MISO, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
   //receive SPI and handle it
     
     test = SPDR;
     SPDR = 1;
      if((SPSR & (1 << SPIF)) != 0) { 
        spiHandler();
        check = true;
      }
      Serial.println(check);
}

//function that sends spi transactions
void spiHandler()
{
  switch (marker)
  {
  case 0:
//    Serial.print(receive);
    dat = SPDR;
    receive = dat;
//    Serial.println(dat);
//    Serial.print(dat);
    if (dat == 1)
    {
      SPDR = 3;
      marker++;
//      Serial.print("received: ");
//      Serial.println(dat);
      break;
    }
    else if (dat == 2) {
      SPDR = 4;
      marker++; 
//      Serial.print("received: ");
//      Serial.println(dat);
      break;
    }

    break;    
  case 1:
    if(receive == 1) {
      pwm = SPDR;
      SPDR = 6;
      Serial.print("pwm: ");
      Serial.println(pwm);
      marker = 0;
      break;
    }
    else if (receive == 2) {
      servoAngle = SPDR;
      SPDR = 7;
      Serial.print("servo: ");
      Serial.println(servoAngle);
      marker = 0;
      break;
    }
    break;
  }
}
