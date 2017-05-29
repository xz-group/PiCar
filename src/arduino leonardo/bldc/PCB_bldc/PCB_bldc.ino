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
int HALLSTATE;
boolean DIRECTION;
/*#define  IS_1  A2
  #define  IS_2  A3
  #define  IS_3  A4
*/

int pwm;
volatile byte rpmcount = 0;
unsigned int rpm = 0;
unsigned long timeold = 0;

void setup() {

  Serial.begin(115200);

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
  
  // Set PWM for pins 9,10,11 to 3.9kHz
  //First clear all three prescaler bits:
  int prescalerVal = 0x07;
  TCCR1B &= ~prescalerVal; 
  //Now set the appropriate prescaler bits:
  int prescalerVal2 = 2; 
  TCCR1B |= prescalerVal2; 
 
  interrupts();
  
  attachInterrupt(2, HALL1_FLAG, CHANGE);
  attachInterrupt(3, HALL2_FLAG, CHANGE);
  attachInterrupt(6, HALL3_FLAG, CHANGE);
}

void HALL1_FLAG() {
  rpmcount++;
  one = !one;
}
void HALL2_FLAG() {
  two = !two;
}
void HALL3_FLAG() {
  three = !three;
}


void loop() {
  if (rpmcount >= 4) {
    noInterrupts();
    //Update RPM every 4 counts, increase this for better RPM resolution,
    //decrease for faster update
    rpm = 30 * 1000000 / (micros() - timeold) * rpmcount;
    timeold = micros();
    rpmcount = 0;
//    Serial.println(rpm);
    interrupts();
  }
  
  HALLSTATE = (4 * one) + (2 * two) + (three);

//PID CONTROLLER
  pwm = rpm/1000;

  if (DIRECTION) {
    CW(HALLSTATE, pwm);
  } else {
    CCW(HALLSTATE, pwm);
  }
/*
  if (STOP){
    digitalWrite(INH_1, LOW);
    digitalWrite(INH_2, LOW);
    digitalWrite(INH_3, LOW);
    }
    */
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
}

void CW(int HALLSTATE, int pwm) {
  switch (HALLSTATE) {
    case 1://001 CA
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, LOW);
      analogWrite(IN_1, pwm); //high
      analogWrite(IN_2, 0); //low
      analogWrite(IN_3, 0); //off
      break;
    case 2://010 BC
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, LOW);
      digitalWrite(INH_3, HIGH);
      analogWrite(IN_1, 0); //low
      analogWrite(IN_2, 0); //off
      analogWrite(IN_3, pwm); //high
      break;
    case 3://011 BA
      digitalWrite(INH_1, LOW);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, HIGH);
      analogWrite(IN_1, 0); //off
      analogWrite(IN_2, 0); //low
      analogWrite(IN_3, pwm); //high
      break;
    case 4://100 AB
      digitalWrite(INH_1, LOW);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, HIGH);
      analogWrite(IN_1, 0); //off
      analogWrite(IN_2, pwm); //high
      analogWrite(IN_3, 0); //low
      break;
    case 5://101 CB
      digitalWrite(INH_1, LOW);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, HIGH);
      analogWrite(IN_1, 0); //off
      analogWrite(IN_2, pwm); //high
      analogWrite(IN_3, 0); //low
      break;
    case 6://110 AC
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, LOW);
      analogWrite(IN_1, 0); //low
      analogWrite(IN_2, pwm); //high
      analogWrite(IN_3, 0); //off
      break;
  }
}

void CCW(int HALLSTATE, int pwm) {
  switch (HALLSTATE)
  {
    case 1://AC O-Y
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, LOW);
      analogWrite(IN_1, 0); //low
      analogWrite(IN_2, pwm); //high
      analogWrite(IN_3, 0); //off
      break;
    case 2:// CB Y-B
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, LOW);
      digitalWrite(INH_3, HIGH);
      analogWrite(IN_1, pwm); //high
      analogWrite(IN_2, 0); //off
      analogWrite(IN_3, 0); //low
      break;
    case 3://AB O-B
      digitalWrite(INH_1, LOW);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, HIGH);
      analogWrite(IN_1, 0); //off
      analogWrite(IN_2, pwm); //high
      analogWrite(IN_3, 0); //low
      break;
    case 4://BA B-O
      digitalWrite(INH_1, LOW);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, HIGH);
      analogWrite(IN_1, 0); //off
      analogWrite(IN_2, 0); //low
      analogWrite(IN_3, pwm); //high

      break;
    case 5://BC B-Y
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, LOW);
      digitalWrite(INH_3, HIGH);
      analogWrite(IN_1, 0); //low
      analogWrite(IN_2, 0); //off
      analogWrite(IN_3, pwm); //high
      break;
    case 6://CA Y-O
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, LOW);
      analogWrite(IN_1, pwm); //high
      analogWrite(IN_2, 0); //low
      analogWrite(IN_3, 0); //off
      break;
  }
}
