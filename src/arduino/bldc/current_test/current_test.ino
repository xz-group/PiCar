#define IN_1  OCR1A//PWM9 yellow
#define IN_2  OCR1B//PWM10 orange
#define IN_3  OCR1C//PWM11 blue

#define  INH_1 6
#define  INH_2 12
#define  INH_3 4

#define  HALL_1 0 // 4 -> HE2
#define  HALL_2 1 // 2 -> HE3
#define  HALL_3 7 // 3 -> HE1

//#define  hallOne 0
//#define  hallTwo 1
//#define  hallThree 7

#define  IS_1  A2
#define  IS_2  A3
#define  IS_3  A4

int HallState1; //Variables for the three hall sensors (3,2,1)
int HallState2;
int HallState3;
int HallVal = 1; //binary value of all 3 hall sensors

void pwm91011configure()
{
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

void CalibrateIS(){
  int I1_offset = analogRead(IS_1);
  int I2_offset = analogRead(IS_2);
  int I3_offset = analogRead(IS_3);
  
  }
void setup() {

  Serial.begin(57600);
  pwm91011configure();

  pwmSet9(0);
  pwmSet10(0);
  pwmSet11(0);
  
  //delay(100);
  //noInterrupts();

  pinMode(INH_1, OUTPUT);
  pinMode(INH_2, OUTPUT);
  pinMode(INH_3, OUTPUT);
  digitalWrite(INH_1, LOW);
  digitalWrite(INH_2, LOW);
  digitalWrite(INH_3, LOW);
  //delay(100);
  //CalibrateIS();
}

void loop() {
  


  if (millis()<3500){
    //test AB
    digitalWrite(INH_1, LOW);
    digitalWrite(INH_2, HIGH); //phase A
    digitalWrite(INH_3, HIGH); //phase B
      IN_1= 0; //low
      IN_2= 50; //high
      IN_3= 0; //off
    Serial.print(analogRead(IS_1));
    Serial.print("\t");
    Serial.print(analogRead(IS_2));
    Serial.print("\t");
    Serial.println(analogRead(IS_3));
    }else{
    digitalWrite(INH_1, LOW);
    digitalWrite(INH_2, LOW); //phase A
    digitalWrite(INH_3, LOW); //phase B
      IN_1= 0; //off
      IN_2= 0; //high
      IN_3= 0; //low
    if(millis()<4000){
    Serial.print(analogRead(IS_1));
    Serial.print("\t");
    Serial.print(analogRead(IS_2));
    Serial.print("\t");
    Serial.println(analogRead(IS_3));
    }}
    //delay(10);
//      IN_1= 0; //low
//      IN_2= 0; //high
//      IN_3= 0; //off

//  if (millis()<8000){
//    fwd(35);
//    }else{
//    digitalWrite(INH_1, LOW);
//    digitalWrite(INH_2, LOW);
//    digitalWrite(INH_3, LOW);
//      IN_1= 0; //low
//      IN_2= 0; //high
//      IN_3= 0; //off
//  }
  
}


void fwd(int pwm) {
  HallState1 = digitalRead(HALL_1);  // read input value from Hall 1
  HallState2  = digitalRead(HALL_2);  // read input value from Hall 2
  HallState3  = digitalRead(HALL_3);  // read input value from Hall 3
  HallVal = (4 * HallState1) + (2 * HallState2) + (HallState3); //Computes the binary value of the 3 Hall sensors
  Serial.println(HallVal);

  switch (HallVal)
  {
    case 1://AC O-Y
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, LOW);
      IN_1= 0; //low
      IN_2= pwm; //high
      IN_3= 0; //off
      break;
    case 2:// CB Y-B
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, LOW);
      digitalWrite(INH_3, HIGH);
      IN_1 = pwm; //high
      IN_2= 0; //off
      IN_3= 0; //low
      break;
    case 3://AB O-B
      digitalWrite(INH_1, LOW);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, HIGH);
      IN_1=0; //off
      IN_2=pwm; //high
      IN_3= 0; //low
      break;
    case 4://BA B-O
      digitalWrite(INH_1, LOW);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, HIGH);
      IN_1= 0; //off
      IN_2= 0; //low
      IN_3= pwm; //high

      break;
    case 5://BC B-Y
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, LOW);
      digitalWrite(INH_3, HIGH);
      IN_1= 0; //low
      IN_2= 0; //off
      IN_3= pwm; //high
      break;
    case 6://CA Y-O
      digitalWrite(INH_1, HIGH);
      digitalWrite(INH_2, HIGH);
      digitalWrite(INH_3, LOW);
      IN_1=pwm; //high
      IN_2= 0; //low
      IN_3= 0; //off
      break;
  }
}
