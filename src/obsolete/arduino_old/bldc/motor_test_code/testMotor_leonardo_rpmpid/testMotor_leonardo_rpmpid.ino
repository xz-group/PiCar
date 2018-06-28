//test on leonardo board
//PCB HALL SENSORS ARE CONNECTED TO D14, SCK, AND MOSI
//ON LEONARDO CONNECTED TO SS(D14),SCK(D15),MOSI(D16)

#define IN_A 9  //Yellow  
#define IN_B 10 //Blue
#define IN_C 11  //Orange

#define INH_A A2 //Yellow
#define INH_B A1 //Blue
#define INH_C A0 //Orange

#define HALL_1 17
#define HALL_2 15
#define HALL_3 16


uint8_t pwm = 30;
bool motorccw = 1;
volatile byte rpmcount = 0;
unsigned int rpm = 0;
unsigned long timeold = 0;
unsigned long RPM_SET = 5000;

int pwm_max = 80;
int Kp = 1;
int Ki = 0.5;
int Kd = 0;

void pciSetup(byte pin)
{
    *digitalPinToPCMSK(pin) |= bit (digitalPinToPCMSKbit(pin));  // enable pin
    PCIFR  |= bit (digitalPinToPCICRbit(pin)); // clear any outstanding interrupt
    PCICR  |= bit (digitalPinToPCICRbit(pin)); // enable interrupt for the group
}

void PWMsetup()
{

  // Initialize global pwm sequence variables
  TCCR1B = TCCR1B & B11111000 | B00000001;// PWM frequency of  31372.55 Hz

  pinMode( IN_A, OUTPUT );
  pinMode( IN_B, OUTPUT );
  pinMode( IN_C, OUTPUT );

  pinMode( INH_A, OUTPUT );
  pinMode( INH_B, OUTPUT );
  pinMode( INH_C, OUTPUT );

  pinMode( HALL_1, INPUT );
  pinMode( HALL_2, INPUT );
  pinMode( HALL_3, INPUT );

  digitalWrite( IN_A, LOW );
  digitalWrite( IN_B, LOW );
  digitalWrite( IN_C, LOW );

  digitalWrite( INH_A, LOW );
  digitalWrite( INH_B, LOW );
  digitalWrite( INH_C, LOW );

}

void setup()
{
  Serial.begin(115200);
    noInterrupts();
    PWMsetup();
    pciSetup(14);
    pciSetup(15);
    pciSetup(16);
    interrupts();
  
  delay(1000);
  //bldc_initial();
}


void loop()
{
    if (rpmcount >= 4) {
      //Serial.println(rpmcount);
    noInterrupts();
    //Update RPM every 4 counts, increase this for better RPM resolution,
    //decrease for faster update
    rpm = 30 * 1000000 / (micros() - timeold) * rpmcount;
    timeold = micros();
    rpmcount = 0;/*
    Serial.println(rpm);
    Serial.println(PWM);
    Serial.println();
    */
    interrupts();  
    pwm = setRPM(pwm, RPM_SET, rpm);
  }
}

int setRPM(float PWM, float RPM_des, float RPM_curr){
  float RPM_err;
  float PWM_new;
  float PWM_err;
  static float last_error=0; //initialize or ignore??
  RPM_err = (abs(RPM_des) - abs(RPM_curr))/100;//why divided by 100??
  PWM_err = Kp*RPM_err + Kd*(RPM_err - last_error);
  PWM_new = PWM+PWM_err;
  last_error = RPM_err;
  // Saturation between 0 and 255
  if(PWM_new > pwm_max)
    PWM_new = pwm_max;
  else if(PWM_new < 20)
    PWM_new = 20;
  /*
  Serial.println(int(PWM_new));
  
  Serial.print("RPM: "); Serial.print(abs(RPM_curr)); 
  Serial.print(" RPM_err: "); Serial.print(RPM_err); 
  Serial.print(" PWM_new: "); Serial.println(PWM_new);
  
  //Serial.print("last_error");Serial.println(last_error);
  */
  return int(PWM_new);
}

ISR (PCINT0_vect) // handle pin change interrupt for PB0-PB7
 {    
  uint8_t hallstate;
  hallstate = digitalRead( HALL_3 ) |
              ( digitalRead( HALL_2 ) << 1 ) |
              ( digitalRead( HALL_1 ) << 2 );

  if ( !motorccw )
    hallstate = ~hallstate;

  switch ( hallstate )
  {
    case 1: // C->A
      PORTF  &= B00011111;
      PORTF  |= B10100000;  //
      analogWrite(IN_A, 0);//LOW
      analogWrite(IN_C, pwm);//HIGH
      analogWrite(IN_B, 255);//G
      
      rpmcount++;
      
      break;
    case 2: // B->C
      PORTF  &= B00011111;
      PORTF  |= B11000000;  //
      analogWrite(IN_B, pwm);//PWM
      analogWrite(IN_C, 0);//LOW
      analogWrite(IN_A, 255);//G
      break;
    case 3:// B->A
      PORTF  &= B00011111;
      PORTF  |= B01100000;  //
      analogWrite(IN_B, pwm);//PWM
      analogWrite(IN_A, 0);//LOW
      analogWrite(IN_C, 255);//G
      break;
    case 4:      // A->B
      PORTF  &= B00011111;
      PORTF  |= B01100000;  //
      analogWrite(IN_A, pwm);//PWM
      analogWrite(IN_B, 0);//LOW
      analogWrite(IN_C, 255);//G 
      break;
    case 5:  //C->B
      PORTF  &= B00011111;
      PORTF  |= B11000000;  //
      analogWrite(IN_C, pwm);//PWM
      analogWrite(IN_A, 255);//G
      analogWrite(IN_B, 0);//LOW
      break;
    case 6: // A->C
      PORTF  &= B00011111;
      PORTF  |= B10100000;  //
      analogWrite(IN_A, pwm);//PWM
      analogWrite(IN_C, 0);//LOW
      analogWrite(IN_B, 255);//G
      break;
  }
 }

 void bldc_initial(){
  int pwm = 30;
    uint8_t hallstate;
  hallstate = digitalRead( HALL_3 ) |
              ( digitalRead( HALL_2 ) << 1 ) |
              ( digitalRead( HALL_1 ) << 2 );

  if ( !motorccw )
    hallstate = ~hallstate;

  switch ( hallstate )
  {
    case 1: // C->A
      PORTF  &= B00011111;
      PORTF  |= B10100000;  //
      analogWrite(IN_A, 0);//LOW
      analogWrite(IN_C, pwm);//HIGH
      analogWrite(IN_B, 255);//G
      break;
    case 2: // B->C
      PORTF  &= B00011111;
      PORTF  |= B11000000;  //
      analogWrite(IN_B, pwm);//PWM
      analogWrite(IN_C, 0);//LOW
      analogWrite(IN_A, 255);//G
      break;
    case 3:// B->A
      PORTF  &= B00011111;
      PORTF  |= B01100000;  //
      analogWrite(IN_B, pwm);//PWM
      analogWrite(IN_A, 0);//LOW
      analogWrite(IN_C, 255);//G
      break;
    case 4:      // A->B
      PORTF  &= B00011111;
      PORTF  |= B01100000;  //
      analogWrite(IN_A, pwm);//PWM
      analogWrite(IN_B, 0);//LOW
      analogWrite(IN_C, 255);//G 
      break;
    case 5:  //C->B
      PORTF  &= B00011111;
      PORTF  |= B11000000;  //
      analogWrite(IN_C, pwm);//PWM
      analogWrite(IN_A, 255);//G
      analogWrite(IN_B, 0);//LOW
      break;
    case 6: // A->C
      PORTF  &= B00011111;
      PORTF  |= B10100000;  //
      analogWrite(IN_A, pwm);//PWM
      analogWrite(IN_C, 0);//LOW
      analogWrite(IN_B, 255);//G
      break;
  }
  }
