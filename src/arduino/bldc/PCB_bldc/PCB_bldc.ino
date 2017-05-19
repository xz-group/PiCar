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

/*#define  IS_1  A1
  #define  IS_2  A2
  #define  IS_3  A3
*/
boolean CW;
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

  // Set PWM for pins 9,10,11 to 3.9kHz
  //First clear all three prescaler bits:
  int prescalerVal = 0x07; //create a variable called prescalerVal and set it equal to the binary number "00000111"                                                       number "00000111"                                                      number "00000111"
  TCCR1B &= ~prescalerVal; //AND the value in TCCR0B with binary number "11111000"
  //Now set the appropriate prescaler bits:
  int prescalerVal2 = 2; //set prescalerVal equal to binary number "00000010"
  TCCR1B |= prescalerVal2; //OR the value in TCCR0B with binary number "00000010"

  attachInterrupt(2, HALL1_ON, RISING);
  attachInterrupt(2, HALL1_OFF, FALLING);
  attachInterrupt(3, HALL2_ON, RISING);
  attachInterrupt(3, HALL2_OFF, FALLING);
  attachInterrupt(6, HALL3_ON, RISING);
  attachInterrupt(6, HALL3_OFF, FALLING);

}

void HALL1_ON(boolean CW, int pwm) {
  rpmcount++;
  if (CW = 1) { //CW  AC
    digitalWrite(INH_1, HIGH);
    digitalWrite(INH_2, HIGH);
    digitalWrite(INH_3, LOW);
    analogWrite(IN_1, 0); //low
    analogWrite(IN_2, pwm); //high
    analogWrite(IN_3, 0); //off
  } else { //CCW  BC
    digitalWrite(INH_1, HIGH);
    digitalWrite(INH_2, LOW);
    digitalWrite(INH_3, HIGH);
    analogWrite(IN_1, 0); //low
    analogWrite(IN_2, 0); //off
    analogWrite(IN_3, pwm); //high
  }
}

void HALL2_ON(boolean CW, int pwm) {
  if (CW = 1) { //CW  BA
    digitalWrite(INH_1, LOW);
    digitalWrite(INH_2, HIGH);
    digitalWrite(INH_3, HIGH);
    analogWrite(IN_1, 0); //off
    analogWrite(IN_2, 0); //low
    analogWrite(IN_3, pwm); //high
  } else { //CCW  CA
    digitalWrite(INH_1, HIGH);
    digitalWrite(INH_2, HIGH);
    digitalWrite(INH_3, LOW);
    analogWrite(IN_1, pwm); //high
    analogWrite(IN_2, 0); //low
    analogWrite(IN_3, 0); //off
  }
}
void HALL3_ON(boolean CW, int pwm) {
  if (CW = 1) { //CW  CB
    digitalWrite(INH_1, HIGH);
    digitalWrite(INH_2, LOW);
    digitalWrite(INH_3, HIGH);
    analogWrite(IN_1, pwm); //high
    analogWrite(IN_2, 0); //off
    analogWrite(IN_3, 0); //low
  } else { //CCW  AB
    digitalWrite(INH_1, LOW);
    digitalWrite(INH_2, HIGH);
    digitalWrite(INH_3, HIGH);
    analogWrite(IN_1, 0); //off
    analogWrite(IN_2, pwm); //high
    analogWrite(IN_3, 0); //low
  }
}
void HALL1_OFF(boolean CW, int pwm) {
  if (CW = 1) { //CW  CA
    digitalWrite(INH_1, HIGH);
    digitalWrite(INH_2, HIGH);
    digitalWrite(INH_3, LOW);
    analogWrite(IN_1, pwm); //high
    analogWrite(IN_2, 0); //low
    analogWrite(IN_3, 0); //off
  } else { //CCW  CB
    digitalWrite(INH_1, LOW);
    digitalWrite(INH_2, HIGH);
    digitalWrite(INH_3, HIGH);
    analogWrite(IN_1, 0); //off
    analogWrite(IN_2, pwm); //high
    analogWrite(IN_3, 0); //low
  }
}

void HALL2_OFF(boolean CW, int pwm) {
  if (CW = 1) { //CW  AB
    digitalWrite(INH_1, LOW);
    digitalWrite(INH_2, HIGH);
    digitalWrite(INH_3, HIGH);
    analogWrite(IN_1, 0); //off
    analogWrite(IN_2, pwm); //high
    analogWrite(IN_3, 0); //low
  } else { //CCW  AC
    digitalWrite(INH_1, HIGH);
    digitalWrite(INH_2, HIGH);
    digitalWrite(INH_3, LOW);
    analogWrite(IN_1, 0); //low
    analogWrite(IN_2, pwm); //high
    analogWrite(IN_3, 0); //off
  }
}

void HALL3_OFF(boolean CW, int pwm) {
  if (CW = 1) { //CW  BC
    digitalWrite(INH_1, HIGH);
    digitalWrite(INH_2, LOW);
    digitalWrite(INH_3, HIGH);
    analogWrite(IN_1, 0); //low
    analogWrite(IN_2, 0); //off
    analogWrite(IN_3, pwm); //high
  } else { //CCW  BA
    digitalWrite(INH_1, LOW);
    digitalWrite(INH_2, HIGH);
    digitalWrite(INH_3, HIGH);
    analogWrite(IN_1, 0); //off
    analogWrite(IN_2, 0); //low
    analogWrite(IN_3, pwm); //high
  }
}


void loop() {
  if (rpmcount >= 4) {
    //Update RPM every 4 counts, increase this for better RPM resolution,
    //decrease for faster update
    rpm = 30 * 1000000 / (micros() - timeold) * rpmcount;
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

}
