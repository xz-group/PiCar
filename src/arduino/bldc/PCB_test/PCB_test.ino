//#define IN_1  OCR1A//PWM9 yellow
//#define IN_2  OCR1B//PWM10 orange
//#define IN_3  OCR1C//PWM11 blue

#define  INH_1 6
#define  INH_2 12
#define  INH_3 4

#define  hallOne 0
#define  hallTwo 1
#define  hallThree 7

#define  IS_1  A2
#define  IS_2  A3
#define  IS_3  A4

volatile boolean one;
volatile boolean two;
volatile boolean three;
volatile int pwm=40;
volatile byte rpmcount = 0;
volatile boolean DIRECTION;
volatile int HALLSTATE;

void pwm91011configure()
{
  // TCCR1A configuration
  //  00 : Channel A disabled D9
  //  00 : Channel B disabled D10
  //  00 : Channel C disabled D11
  //  01 : Fast PWM 8 bit
  TCCR1A = 1;
  TCCR1B = 0x02; // Clock mode 8khz and Fast PWM 8 bit. 3.9khz
  TCCR1C = 0; // TCCR1C configuration
}

void pwmSet9(int value)// Set PWM to D9
{
  OCR1A = value; // Set PWM value
  DDRB |= 1 << 5; // Set Output Mode B5
  TCCR1A |= 0x80; // Activate channel
}

void pwmSet10(int value)// Set PWM to D10
{
  OCR1B = value; // Set PWM value
  DDRB |= 1 << 6; // Set Output Mode B6
  TCCR1A |= 0x20; // Set PWM value
}

void pwmSet11(int value)// Set PWM to D11
{
  OCR1C = value; // Set PWM value
  DDRB |= 1 << 7; // Set Output Mode B7
  TCCR1A |= 0x08; // Set PWM value
}
/*
  void UPDATE_PWM(){

  //analogRead(IS); Calculate current
  //if current over limits, shut down; if current ok, update PWM
  //Calculate  RPM
  //APPLY PID (REFERNENCE RPM)
  }
*/
void HALL1_FLAG() {
  rpmcount++;
  one = !one;
  HALLSTATE = one*4 + two *2 + three;
 // HALLSTATE = (one << 2) & (two << 1) & three;
  switch (HALLSTATE)
  {
    case 1://AC O-Y
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, LOW);
      OCR1A = 0;//low
      OCR1B = pwm;//high
      OCR1C = 0;//off
      break;
    case 2:// CB Y-B
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, LOW);
      digitalWrite(INH_3, HIGH);
      OCR1A = pwm;//high
      OCR1B = 0;//off
      OCR1C = 0;//low
      break;
    case 3://AB O-B
      digitalWrite(INH_1, LOW);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, HIGH);
      OCR1A = 0;//off
      OCR1B = pwm;//high
      OCR1C = 0;//low
      break;
    case 4://BA B-O
      digitalWrite(INH_1, LOW);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, HIGH);
      OCR1A = 0;//off
      OCR1B = 0;//low
      OCR1C = pwm;//high
      break;
    case 5://BC B-Y
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, LOW);
      digitalWrite(INH_3, HIGH);
      OCR1A = 0;//low
      OCR1B = 0;//off
      OCR1C = pwm;//high
      break;
    case 6://CA Y-O
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, LOW);
      OCR1A = pwm;//high
      OCR1B = 0;//low
      OCR1C = 0;//off
      break;
  }
  
}
void HALL2_FLAG() {
  two = !two;
  HALLSTATE = one*4 + two *2 + three;
 // HALLSTATE = (one << 2) & (two << 1) & three;
  switch (HALLSTATE)
  {
    case 1://AC O-Y
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, LOW);
      OCR1A = 0;//low
      OCR1B = pwm;//high
      OCR1C = 0;//off
      break;
    case 2:// CB Y-B
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, LOW);
      digitalWrite(INH_3, HIGH);
      OCR1A = pwm;//high
      OCR1B = 0;//off
      OCR1C = 0;//low
      break;
    case 3://AB O-B
      digitalWrite(INH_1, LOW);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, HIGH);
      OCR1A = 0;//off
      OCR1B = pwm;//high
      OCR1C = 0;//low
      break;
    case 4://BA B-O
      digitalWrite(INH_1, LOW);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, HIGH);
      OCR1A = 0;//off
      OCR1B = 0;//low
      OCR1C = pwm;//high
      break;
    case 5://BC B-Y
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, LOW);
      digitalWrite(INH_3, HIGH);
      OCR1A = 0;//low
      OCR1B = 0;//off
      OCR1C = pwm;//high
      break;
    case 6://CA Y-O
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, LOW);
      OCR1A = pwm;//high
      OCR1B = 0;//low
      OCR1C = 0;//off
      break;
  }
}
void HALL3_FLAG() {
  three = !three;
  HALLSTATE = one*4 + two *2 + three;
 // HALLSTATE = (one << 2) & (two << 1) & three;
  switch (HALLSTATE)
  {
    case 1://AC O-Y
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, LOW);
      OCR1A = 0;//low
      OCR1B = pwm;//high
      OCR1C = 0;//off
      break;
    case 2:// CB Y-B
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, LOW);
      digitalWrite(INH_3, HIGH);
      OCR1A = pwm;//high
      OCR1B = 0;//off
      OCR1C = 0;//low
      break;
    case 3://AB O-B
      digitalWrite(INH_1, LOW);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, HIGH);
      OCR1A = 0;//off
      OCR1B = pwm;//high
      OCR1C = 0;//low
      break;
    case 4://BA B-O
      digitalWrite(INH_1, LOW);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, HIGH);
      OCR1A = 0;//off
      OCR1B = 0;//low
      OCR1C = pwm;//high
      break;
    case 5://BC B-Y
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, LOW);
      digitalWrite(INH_3, HIGH);
      OCR1A = 0;//low
      OCR1B = 0;//off
      OCR1C = pwm;//high
      break;
    case 6://CA Y-O
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, LOW);
      OCR1A = pwm;//high
      OCR1B = 0;//low
      OCR1C = 0;//off
      break;
  }
}

void setup() {

  Serial.begin(57600);
  //delay(100);
  noInterrupts();

  pinMode(INH_1, OUTPUT);
  pinMode(INH_2, OUTPUT);
  pinMode(INH_3, OUTPUT);
  digitalWrite(INH_1, LOW);
  digitalWrite(INH_2, LOW);
  digitalWrite(INH_3, LOW);

  one = digitalRead(hallOne);//read initial hall sensors
  two = digitalRead(hallTwo);
  three = digitalRead(hallThree);

  pwm91011configure();

  pwmSet9(0);
  pwmSet10(0);
  pwmSet11(0);
  HALLSTATE = one*4 + two *2 + three;
 // HALLSTATE = (one << 2) & (two << 1) & three;
  switch (HALLSTATE)
  {
    case 1://AC O-Y
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, LOW);
      OCR1A = 0;//low
      OCR1B = pwm;//high
      OCR1C = 0;//off
      break;
    case 2:// CB Y-B
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, LOW);
      digitalWrite(INH_3, HIGH);
      OCR1A = pwm;//high
      OCR1B = 0;//off
      OCR1C = 0;//low
      break;
    case 3://AB O-B
      digitalWrite(INH_1, LOW);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, HIGH);
      OCR1A = 0;//off
      OCR1B = pwm;//high
      OCR1C = 0;//low
      break;
    case 4://BA B-O
      digitalWrite(INH_1, LOW);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, HIGH);
      OCR1A = 0;//off
      OCR1B = 0;//low
      OCR1C = pwm;//high
      break;
    case 5://BC B-Y
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, LOW);
      digitalWrite(INH_3, HIGH);
      OCR1A = 0;//low
      OCR1B = 0;//off
      OCR1C = pwm;//high
      break;
    case 6://CA Y-O
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, LOW);
      OCR1A = pwm;//high
      OCR1B = 0;//low
      OCR1C = 0;//off
      break;
  }
  interrupts();
  attachInterrupt(digitalPinToInterrupt(0), HALL1_FLAG, CHANGE);
  attachInterrupt(digitalPinToInterrupt(1), HALL2_FLAG, CHANGE);
  attachInterrupt(digitalPinToInterrupt(7), HALL3_FLAG, CHANGE);

}

void loop() {

  //
  //  Serial.print(analogRead(IS_1));
  //  Serial.print("\t");
  //  Serial.print(analogRead(IS_2));
  //  Serial.print("\t");
  //  Serial.println(analogRead(IS_3));
//Serial.println(HALLSTATE);
//  Serial.print(one);
//  Serial.print(two);
//  Serial.println(three);
//  Serial.println("################");
//  delay(100);
  if (millis() > 10000) {
    digitalWrite(INH_1, LOW);
    digitalWrite(INH_2, LOW);
    digitalWrite(INH_3, LOW);
  }
}



