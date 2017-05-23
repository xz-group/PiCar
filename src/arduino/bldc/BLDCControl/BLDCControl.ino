/*http://playground.arduino.cc/Main/ReadingRPM
  http://elimelecsarduinoprojects.blogspot.com/2013/06/measure-rpms-arduino.html
*/

#include "PWM.h"
#define  IN_1  9 //yellow
#define  IN_2  10 //orange
#define  IN_3  11//blue
#define  INH_1 5
#define  INH_2 6
#define  INH_3 7
#define  HALL_1 4 // 4 -> HE2
#define  HALL_2 2 // 2 -> HE3
#define  HALL_3 3 // 3 -> HE1
/*#define  IS_1  A1
  #define  IS_2  A2
  #define  IS_3  A3
*/
int HallState1; //Variables for the three hall sensors (3,2,1)
int HallState2;
int HallState3;
int HallVal = 1; //binary value of all 3 hall sensors
double PWM = 50;
int pwm_max = 100;
int a;
int Kp = 6;
int Ki = 1;
int Kd = 0;


volatile byte rpmcount = 0;
volatile byte rpmcount2 = 0;
float rpm = 0;
float rpm2 = 0;
double rpm_avg = 0;
unsigned long timeold = 0;
unsigned long timeold2 = 0;
float RPM_set = 3000;

void setup() {

  Serial.begin(115200);

//  detachInterrupt(0);
  pinMode(IN_1, OUTPUT);
  pinMode(IN_2, OUTPUT);
  pinMode(IN_3, OUTPUT);
  pinMode(INH_1, OUTPUT);
  pinMode(INH_2, OUTPUT);
  pinMode(INH_3, OUTPUT);
  pinMode(HALL_1, INPUT);
  pinMode(HALL_2, INPUT);
  pinMode(HALL_3, INPUT);

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

  attachInterrupt(0, magnet_detect, RISING); //enable interrupt
  attachInterrupt(1, magnet_detect_2, RISING); //enable interrupt
  
  Serial.println("Waiting 3 seconds...");
  delay(3*1000);
  Serial.println("Ready");
}


void loop() {
  /*
    //update rpm every second
    if (millis() - timeold == 1000){  //Uptade every one second, this will be equal to reading frecuency (Hz).
    detachInterrupt(0);    //Disable interrupt when calculating
    rpm = rpmcount * 30;  // Convert frecuency to RPM, note: this works for one interruption per full rotation. For two interrups per full rotation use rpmcount * 30.
    Serial.print("RPM =\t"); //print the word "RPM" and tab.
    Serial.print(rpm); // print the rpm value.
    Serial.print("\t Hz=\t"); //print the word "Hz".
    Serial.println(rpmcount); //print revolutions per second or Hz. And print new line or enter.
    rpmcount = 0; // Restart the RPM counter
    timeold = millis(); // Uptade lasmillis
    attachInterrupt(0, magnet_detect, RISING); //enable interrupt
    }
  */
  
  if (rpmcount >= 1) { //Update RPM every 4 counts, increase this for better RPM resolution,
    //decrease for faster update
    rpm = 30.0 * 1000 / (millis() - timeold) * rpmcount;
    timeold = millis();
    rpmcount = 0;
    //Serial.print(int(rpm));
    
    //fwd(40);
  }
  if (rpmcount2 >= 1) { //Update RPM every 4 counts, increase this for better RPM resolution,
    //decrease for faster update
    rpm2 = 30.0 * 1000 / (millis() - timeold2) * rpmcount2;
    timeold2 = millis();
    rpmcount2 = 0;
    //Serial.print("\t");
    //Serial.println(int(rpm2));
    
    //fwd(40);
  }
  rpm_avg = (rpm + rpm2)/2;

  
  //Serial.println(int(rpm_avg));
  
  //Serial.println(PWM);
  fwd(PWM);
  PWM = setRPM(PWM, RPM_set, abs(rpm_avg));
  //fwd(PWM);
  //rpm_old = rpm;
  //attachInterrupt(0, magnet_detect, RISING);
  /*
    if(Serial.available()>0){
       a = Serial.read();
       Serial.println(a);
    }
       if (a == 48){//ingput 0, turns off
             digitalWrite(INH_1, LOW);
             digitalWrite(INH_2, LOW);
             digitalWrite(INH_3, LOW);

        }
  */
  /*      Serial.print("current 1: ");
        Serial.println(analogRead(IS_1));
        Serial.print("current 2: ");
        Serial.println(analogRead(IS_2));
        Serial.print("current 3: ");
        Serial.println(analogRead(IS_3));
  */

  Serial.flush();
}

int fwd(int pwm) {
  HallState1 = digitalRead(HALL_1);  // read input value from Hall 1
  HallState2  = digitalRead(HALL_2);  // read input value from Hall 2
  HallState3  = digitalRead(HALL_3);  // read input value from Hall 3
  HallVal = (4 * HallState1) + (2 * HallState2) + (HallState3); //Computes the binary value of the 3 Hall sensors
//  Serial.println(HallVal);

  switch (HallVal)
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

// using PID to drive motor to desired RPM
int setRPM(float PWM, float RPM_des, float RPM_curr){
  float RPM_err;
  float PWM_new;
  float PWM_err;
  static float last_error=0; 
  RPM_err = (abs(RPM_des) - abs(RPM_curr))/100;
  PWM_err = Kp*RPM_err + Kd*(RPM_err - last_error);
  PWM_new = PWM+PWM_err;
  last_error = RPM_err;
  // Saturation between 0 and 255
  if(PWM_new > pwm_max)
    PWM_new = pwm_max;
  else if(PWM_new < 20)
    PWM_new = 20;
  //Serial.println(int(PWM_new));
  //Serial.print("RPM: "); Serial.print(abs(RPM_curr)); 
  //Serial.print(" RPM_err: "); Serial.print(RPM_err); 
  //Serial.print(" PWM_new: "); Serial.println(PWM_new);
    
  return int(PWM_new);
}

void magnet_detect()
{
  rpmcount++;
//  Serial.println("detect");
}

void magnet_detect_2()
{
  rpmcount2++;
//  Serial.println("detect");
}
