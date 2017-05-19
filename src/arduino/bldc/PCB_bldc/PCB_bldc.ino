#include <PWM.h>
#define  IN_1  9 //yellow
#define  IN_2  10 //orange
#define  IN_3  11//blue
#define  INH_1 6
#define  INH_2 12
#define  INH_3 4

#define  hallOne 0
#define  hallTwo 1
#define  hallThree 7

volatile int one;
volatile int two;
volatile int three;
/*#define  IS_1  A1
  #define  IS_2  A2
  #define  IS_3  A3
*/

int pwm;
volatile byte rpmcount = 0;
unsigned int rpm = 0;
unsigned long timeold = 0;

void setup() {

  Serial.begin(115200);
  //  attachInterrupt(0, magnet_detect, RISING);

  pinMode(IN_1, OUTPUT);
  pinMode(IN_2, OUTPUT);
  pinMode(IN_3, OUTPUT);
  pinMode(INH_1, OUTPUT);
  pinMode(INH_2, OUTPUT);
  pinMode(INH_3, OUTPUT);

  digitalWrite(INH_1, LOW);
  digitalWrite(INH_2, LOW);
  digitalWrite(INH_3, LOW);
  
  one = digitalRead(hallOne);
  two = digitalRead(hallTwo);
  three = digitalRead(hallThree);



  noInterrupts();

  // Set PWM for pins 9,10 to 3.9kHz
  //First clear all three prescaler bits:
  int prescalerVal = 0x07; //create a variable called prescalerVal and set it equal to the binary number "00000111"                                                       number "00000111"                                                      number "00000111"
  TCCR1B &= ~prescalerVal; //AND the value in TCCR0B with binary number "11111000"

  //Now set the appropriate prescaler bits:
  // int prescalerVal2 = 2; //set prescalerVal equal to binary number "00000010"
  TCCR1B |= B00000010; //OR the value in TCCR0B with binary number "00000010"

  // Set PWM for pins 3,11 to 3.9kHz (Only pin 11 is used in this program)
  //First clear all three prescaler bits:
  TCCR2B &= ~prescalerVal; //AND the value in TCCR0B with binary number "11111000"

  //Now set the appropriate prescaler bits:

  TCCR2B |= B00000010; //OR the value in TCCR0B with binary number "00000010"//First clear all three prescaler bits:

attachInterrupt(2, HALL1_ON(CW,pwm), RISING);
attachInterrupt(2, HALL1_OFF(CW,pwm), FALLING);
attachInterrupt(3, HALL2_ON(CW,pwm), RISING);
attachInterrupt(3, HALL2_OFF(CW,pwm), FALLING);
attachInterrupt(6, HALL3_ON(CW,pwm), RISING);
attachInterrupt(6, HALL3_OFF(CW,pwm), FALLING);

}

void HALL1_ON(boolean CW){
  if (CW = 1){//CW  AC
        digitalWrite(INH_1, HIGH);
        digitalWrite(INH_2, HIGH);
        digitalWrite(INH_3, LOW);
        analogWrite(IN_1, 0); //low
        analogWrite(IN_2, pwm); //high
        analogWrite(IN_3, 0); //off
    }else{//CCW  BC
        digitalWrite(INH_1, HIGH);
        digitalWrite(INH_2, LOW);
        digitalWrite(INH_3, HIGH);
        analogWrite(IN_1, 0); //low
        analogWrite(IN_2, 0); //off
        analogWrite(IN_3, pwm); //high
      }
  }

void HALL2_ON(boolean CW,int pwm){
  if (CW = 1){//CW  BA
        digitalWrite(INH_1, LOW);
        digitalWrite(INH_2, HIGH);
        digitalWrite(INH_3, HIGH);
        analogWrite(IN_1, 0); //off
        analogWrite(IN_2, 0); //low
        analogWrite(IN_3, pwm); //high
    }else{//CCW  CA
        digitalWrite(INH_1, HIGH);
        digitalWrite(INH_2, HIGH);
        digitalWrite(INH_3, LOW);
        analogWrite(IN_1, pwm); //high
        analogWrite(IN_2, 0); //low
        analogWrite(IN_3, 0); //off
      }
  }

ISR(PCINT1_vect)        // interrupt service routine
{
  one = digitalRead(A1);
  two = digitalRead(A2);
  three = digitalRead(A3);
  //  Serial.println("pin changed");
  if(one==1 && two==0 && three==0){
    rpmcount++;
//    Serial.println("add one");
    }
}


void loop() {
    if (rpmcount >= 4) { 
     //Update RPM every 4 counts, increase this for better RPM resolution,
     //decrease for faster update
     rpm = 30*1000000/(micros() - timeold)*rpmcount;
     timeold = micros();
     rpmcount = 0;
     Serial.println(rpm);
   }

//  fwd(75);
  /*
    if (millis() - timeold == 1000){
    noInterrupts();2
    rpm = rpmcount * 30;
    Serial.print(rpm);
    rpmcount = 0; // Restart the RPM counter
    timeold = millis();
    interrupts();
    }
  */

  /* 
        Serial.println(analogRead(IS_1));
        Serial.println(analogRead(IS_2));
        Serial.println(analogRead(IS_3));
  */

}

int fwd(int pwm) {
  /*
    Serial.print("hall sensor:  ");
    Serial.print(one);
    Serial.print("   ");
    Serial.print(two);
    Serial.print("   ");
    Serial.println(three);
    Serial.println("   ");
  */
  if (one == 0) {
    if (two == 1) {
      if (three == 0) { //010 CB Y-B h1=0,h2=1,h3=0
        digitalWrite(INH_1, HIGH);
        digitalWrite(INH_2, LOW);
        digitalWrite(INH_3, HIGH);
        analogWrite(IN_1, pwm); //high
        analogWrite(IN_2, 0); //off
        analogWrite(IN_3, 0); //low
        //        Serial.println("CB");
      } else { // 011 AB O-B h1=0,h2=1,h3=1
        digitalWrite(INH_1, LOW);
        digitalWrite(INH_2, HIGH);
        digitalWrite(INH_3, HIGH);
        analogWrite(IN_1, 0); //off
        analogWrite(IN_2, pwm); //high
        analogWrite(IN_3, 0); //low
        //        Serial.println("AB");
      }
    }
    if (two == 0) {
      if (three == 1) { //001 AC O-Y h1=0,h2=0,h3=1
        digitalWrite(INH_1, HIGH);
        digitalWrite(INH_2, HIGH);
        digitalWrite(INH_3, LOW);
        analogWrite(IN_1, 0); //low
        analogWrite(IN_2, pwm); //high
        analogWrite(IN_3, 0); //off
        //       Serial.println("AC");
      }
    }
  }

  if (one == 1) {
    if (two == 0) {
      if (three == 1) { //101 BC B-Y
        digitalWrite(INH_1, HIGH);
        digitalWrite(INH_2, LOW);
        digitalWrite(INH_3, HIGH);
        analogWrite(IN_1, 0); //low
        analogWrite(IN_2, 0); //off
        analogWrite(IN_3, pwm); //high
        //        Serial.println("BC");
      } else { //100 BA B-O
        digitalWrite(INH_1, LOW);
        digitalWrite(INH_2, HIGH);
        digitalWrite(INH_3, HIGH);
        analogWrite(IN_1, 0); //off
        analogWrite(IN_2, 0); //low
        analogWrite(IN_3, pwm); //high
        //       Serial.println("BA");
      }
    }
    if (two == 1) { //110 CA Y-O
      if (three == 0) {
        digitalWrite(INH_1, HIGH);
        digitalWrite(INH_2, HIGH);
        digitalWrite(INH_3, LOW);
        analogWrite(IN_1, pwm); //high
        analogWrite(IN_2, 0); //low
        analogWrite(IN_3, 0); //off
        //     Serial.println("CA");
      }
    }
  }
}
/*
  void magnet_detect()
  {
   rpmcount++;
   Serial.println("detect");
  }
*/
void pciSetup(byte pin)
{
  *digitalPinToPCMSK(pin) |= bit (digitalPinToPCMSKbit(pin));  // enable pin
  PCIFR  |= bit (digitalPinToPCICRbit(pin)); // clear any outstanding interrupt
  PCICR  |= bit (digitalPinToPCICRbit(pin)); // enable interrupt for the group
}
