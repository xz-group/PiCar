// Direct PWM change variables
#define IN_1  OCR1A//PWM9  9 //yellow
#define IN_2  OCR1B//PWM10  10 //orange
#define IN_3  OCR1C//PWM11  11//blue

#define  INH_1 6
#define  INH_2 12
#define  INH_3 4

#define  hallOne 0
#define  hallTwo 1
#define  hallThree 7

#define  IS_1  A2
#define  IS_2  A3
#define  IS_3  A4
  
volatile int one;
volatile int two;
volatile int three;
volatile byte rpmcount = 0;

int HALLSTATE = 0;

void pwm91011configure(int mode)//1:62500 Hz  2:7812Hz  3:976Hz 4:244Hz
{
// TCCR1A configuration
//  00 : Channel A disabled D9
//  00 : Channel B disabled D10
//  00 : Channel C disabled D11
//  01 : Fast PWM 8 bit
TCCR1A=1;
TCCR1B=mode|0x08;  // TCCR1B configuration// Clock mode and Fast PWM 8 bit
TCCR1C=0;// TCCR1C configuration
}

void pwmSet9(int value)// Set PWM to D9
{
OCR1A=value;   // Set PWM value
DDRB|=1<<5;    // Set Output Mode B5
TCCR1A|=0x80;  // Activate channel
}

void pwmSet10(int value)// Set PWM to D10
{
OCR1B=value;   // Set PWM value
DDRB|=1<<6;    // Set Output Mode B6
TCCR1A|=0x20;  // Set PWM value
}

void pwmSet11(int value)// Set PWM to D11
{
OCR1C=value;   // Set PWM value
DDRB|=1<<7;    // Set Output Mode B7
TCCR1A|=0x08;  // Set PWM value
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

void setup() {
  Serial.begin(115200);
  noInterrupts();
      digitalWrite(INH_1, LOW);
      digitalWrite(INH_2, LOW);
      digitalWrite(INH_3, LOW);
  one = digitalRead(hallOne);//read initial hall sensors
  two = digitalRead(hallTwo);
  three = digitalRead(hallThree);
  pwm91011configure(2);//set timer1 7810 Hz
  interrupts();
  
  attachInterrupt(digitalPinToInterrupt(0), HALL1_FLAG, CHANGE);
  attachInterrupt(digitalPinToInterrupt(1), HALL2_FLAG, CHANGE);
  attachInterrupt(digitalPinToInterrupt(7), HALL3_FLAG, CHANGE);
}

void loop() {
  HALLSTATE +=1;
  if (HALLSTATE >= 7){
    HALLSTATE = 1;
    }
    delay(100);
//HALLSTATE = (4 * one) + (2 * two) + (three);
Serial.println(HALLSTATE);
//Serial.print(one);
//Serial.print(two);
//Serial.println(three);
//Serial.println("################");
//delay(100);
CCW(HALLSTATE, 30);
}

void CCW(int HALLSTATE, int pwm) {
  switch (HALLSTATE)
  {
    case 1://AC O-Y
//      digitalWrite(INH_1, HIGH);
//      digitalWrite(INH_2, HIGH);
//      digitalWrite(INH_3, LOW);
      pwmSet9(0);//low
      pwmSet10(pwm);//high
      pwmSet11(0);//off
      break;
    case 2:// CB Y-B
//      digitalWrite(INH_1, HIGH);
//      digitalWrite(INH_2, LOW);
//      digitalWrite(INH_3, HIGH);
      pwmSet9(pwm);//high
      pwmSet10(0);//off
      pwmSet11(0);//low
      break;
    case 3://AB O-B
//      digitalWrite(INH_1, LOW);
//      digitalWrite(INH_2, HIGH);
//      digitalWrite(INH_3, HIGH);
      pwmSet9(0);//off
      pwmSet10(pwm);//high
      pwmSet11(0);//low
      break;
    case 4://BA B-O
//      digitalWrite(INH_1, LOW);
//      digitalWrite(INH_2, HIGH);
//      digitalWrite(INH_3, HIGH);
      pwmSet9(0);//off
      pwmSet10(0);//low
      pwmSet11(pwm);//high
      break;
    case 5://BC B-Y
//      digitalWrite(INH_1, HIGH);
//      digitalWrite(INH_2, LOW);
//      digitalWrite(INH_3, HIGH);
      pwmSet9(0);//low
      pwmSet10(0);//off
      pwmSet11(pwm);//high
      break;
    case 6://CA Y-O
//      digitalWrite(INH_1, HIGH);
//      digitalWrite(INH_2, HIGH);
//      digitalWrite(INH_3, LOW);
      pwmSet9(pwm);//high
      pwmSet10(0);//low
      pwmSet11(0);//off
      break;
  }
}

