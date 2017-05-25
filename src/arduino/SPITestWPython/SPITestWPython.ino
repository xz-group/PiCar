#include <Servo.h>
#include <SPI.h>

Servo servo;
Servo esc;

int pwm;
int servoAngle;
int marker;
unsigned char dat;
byte receive;

//ISR(SPI_STC_vect) {
//  switchVal = pulseIn(KILL_SWITCH, HIGH);
//}

void setup() {
  // put your setup code here, to run once:
  
  //Setup SPI
  SPCR |= _BV(SPE);
  pinMode(MISO, OUTPUT);


  //attach servo and ESC to pins
  servo.attach(3);
  esc.attach(5);

  //Servo starts at 90 degrees
  servo.write(90);

  //Uncomment to calibrate the ESC
//  while(millis() < 6000) {
//    esc.writeMicroseconds(2000);
//    Serial.println("high");
//  }
//  while(millis() < 12000) {
//    esc.writeMicroseconds(1000);
//    Serial.println("low");
//  }
//  while(millis() < 18000) {
//    esc.writeMicroseconds(1500);
//    Serial.println("middle");
//  }
}

void loop() {
  // put your main code here, to run repeatedly:   
   
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
   esc.writeMicroseconds(pwm*50);
   servo.write(servoAngle);

}

void spiHandler()
{
  switch (marker)
  {
  case 0:
//    Serial.print(receive);
    dat = SPDR;
    receive = dat;
    Serial.println(dat);
//    Serial.print(dat);
    if (dat == 1)
    {
      SPDR = 1;
      marker++;
    }
    else if (dat == 2) {
      SPDR = 2;
      marker++; 
    }
    else {
//      Serial.println("dat is wrong 1");
    }
    break;    
  case 1:
    if(receive == 1) {
      pwm = SPDR;
      SPDR = pwm;
//      Serial.print("pwm: ");
//      Serial.println(pwm);
      marker = 0;
    }
    else if (receive == 2) {
      servoAngle = SPDR;
      SPDR = servoAngle;
//      Serial.print(servoAngle);
//      Serial.print("servo: ");
      marker = 0;
    }
    else {
//      Serial.println("dat is wrong 2"); 
    }
    break;
  }
}
