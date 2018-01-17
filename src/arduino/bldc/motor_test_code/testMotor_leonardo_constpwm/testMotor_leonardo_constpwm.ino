//test on leonardo board
//PCB HALL SENSORS ARE CONNECTED TO D14, SCK, AND MOSI
//ON LEONARDO CONNECTED TO MISO(D17),SCK(D15),MOSI(D16)

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
uint16_t revcount = 0;
bool motorccw = 1;

void setup()
{
  Serial.begin( 9600 );
  PWMsetup();
  delay(1000);
  isrHallSeq();
}

void loop()
{
 

  isrHallSeq();

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


void isrHallSeq()
{
  uint8_t hallstate;
  revcount++;
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

