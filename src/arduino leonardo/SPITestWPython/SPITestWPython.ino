#include <Servo.h>
#include <SPI.h>

#define MAX_SPEED 300

Servo servo;
Servo esc;

int pwm;
int servoAngle;
int marker;
unsigned char dat;
byte receive;
bool kill = true;

void setup() {
  // put your setup code here, to run once:
  //uncomment for debugging
  Serial.begin(115200);
  //Setup SPI
  SPCR |= _BV(SPE);
  pinMode(MISO, OUTPUT);

  //attach servo and ESC to pins
  servo.attach(3);
  esc.attach(5);

  //Servo starts at 90 degrees
  servo.write(90);

  //Uncomment to calibrate the ESC
  while(millis() < 6000) {
    esc.writeMicroseconds(2000);
    Serial.println("high");
  }
  while(millis() < 12000) {
    esc.writeMicroseconds(1000);
    Serial.println("low");
  }
  while(millis() < 18000) {
    esc.writeMicroseconds(1500);
    Serial.println("middle");
  }
}

void loop() {
  // put your main code here, to run repeatedly:
   if(millis() < 7000) {
   //receive SPI and handle it
      if((SPSR & (1 << SPIF)) != 0) { 
        spiHandler();
      }
   
   

      //Servo angle saturation
      if(servoAngle < 50) {
         servoAngle = 50;
      }
      if(servoAngle > 130) {
         servoAngle = 130;
      }
   
      //write values to servo and esc
      esc.writeMicroseconds(1500 + MAX_SPEED*pwm/164.0);
//      Serial.print("pwm: ");
//      Serial.println(1500 + MAX_SPEED*((float)pwm)/164.0);
      servo.write(servoAngle);
//      Serial.print("servo: ");
//      Serial.println(servoAngle);
      
   }
   else {
      esc.writeMicroseconds(1500);
      servo.write(90);
      Serial.println("killed");
   }
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
    else if (dat == 3) {
      SPDR = 5;
      marker++;
      break;
    }
    else if (dat == 4) {
      kill = false;
      servoAngle = 90;
      break;
    }
    else {
//      Serial.println("dat is wrong 1");
//      Serial.print("error: ");
//      Serial.println(dat);
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
    else if (receive == 3) {
      pwm = SPDR;
      SPDR = 8;
      pwm = -pwm;
      marker = 0;
      break;
    }
    else {
//      Serial.println("dat is wrong 2");
//      Serial.print("error2: ");
//      Serial.println(dat); 
    }
    break;
  }
}
