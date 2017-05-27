#define DEBUG 0

#define IN_A 9
#define IN_B 10
#define IN_C 11

#define INH_A 6
#define INH_B 12
#define INH_C 4

#define HALL_1 0
#define HALL_2 1
#define HALL_3 7

#define IS_A A2
#define IS_B A3
#define IS_C A4

/*
  A - Orange
  B - Blue
  C - Yellow
*/

#define setPWMA( value ) ( OCR1A = (uint8_t) value )
#define setPWMB( value ) ( OCR1B = (uint8_t) value )
#define setPWMC( value ) ( OCR1C = (uint8_t) value )


volatile uint8_t pwm = 0;
volatile uint16_t revcount = 0;

/*
  void UPDATE_PWM(){

  //analogRead(IS); Calculate current
  //if current over limits, shut down; if current ok, update PWM
  //Calculate  RPM
  //APPLY PID (REFERNENCE RPM)
  }
*/


void isrHallSeq()
{
  uint8_t hallstate = digitalRead( HALL_3 ) |
    ( digitalRead( HALL_2 ) << 1 ) |
    ( digitalRead( HALL_1 ) << 2 );

  revcount++;

  switch( hallstate )
  {
  case 1: // A->C
    digitalWrite( INH_A, HIGH );
    digitalWrite( INH_B, LOW );
    digitalWrite( INH_C, HIGH );
    setPWMA( pwm );
    setPWMB( 0 );
    setPWMC( 0 );
    break;
  case 2: // C->B
    digitalWrite( INH_A, LOW );
    digitalWrite( INH_B, HIGH );
    digitalWrite( INH_C, HIGH );
    setPWMA( 0 );
    setPWMB( 0 );
    setPWMC( pwm );
    break;
  case 3: // A->B
    digitalWrite( INH_A, HIGH );
    digitalWrite( INH_B, HIGH );
    digitalWrite( INH_C, LOW );
    setPWMA( pwm );
    setPWMB( 0 );
    setPWMC( 0 );
    break;
  case 4: // B->A
    digitalWrite( INH_A, HIGH );
    digitalWrite( INH_B, HIGH );
    digitalWrite( INH_C, LOW );
    setPWMA( 0 );
    setPWMB( pwm );
    setPWMC( 0 );
    break;
  case 5: // B->C
    digitalWrite( INH_A, LOW );
    digitalWrite( INH_B, HIGH );
    digitalWrite( INH_C, HIGH );
    setPWMA( 0 );
    setPWMB( pwm );
    setPWMC( 0 );
    break;
  case 6: // C->A
    digitalWrite( INH_A, HIGH );
    digitalWrite( INH_B, LOW );
    digitalWrite( INH_C, HIGH );
    setPWMA( 0 );
    setPWMB( 0 );
    setPWMC( pwm );
    break;
  }
}


void setup()
{
  noInterrupts();

#if DEBUG
  Serial.begin( 57600 );
#endif

  setPWMA( 0 );
  setPWMB( 0 );
  setPWMC( 0 );

  // Enable all compare outputs, Fast PWM 8 bit
  TCCR1A = bit( COM1A1 ) | bit( COM1B1 ) | bit( COM1C1 ) | bit( WGM10 ); // Sec. 14.10.1, Table 14.2
  // Prescaler clock/8, Fast PWM 8 bit -> 7.8KHz PWM
  TCCR1B = bit( WGM12 ) | bit( CS11 ); // Sec. 14.10.3, Tables 14.4-5
  TCCR1C = 0; // Sec. 14.10.5

  // Set port B compare pins as output
  pinMode( IN_A, OUTPUT );
  pinMode( IN_B, OUTPUT );
  pinMode( IN_C, OUTPUT );

  pinMode( INH_A, OUTPUT );
  pinMode( INH_B, OUTPUT );
  pinMode( INH_C, OUTPUT );

  digitalWrite( INH_A, LOW );
  digitalWrite( INH_B, LOW );
  digitalWrite( INH_C, LOW );

  pinMode( HALL_1, INPUT );
  pinMode( HALL_2, INPUT );
  pinMode( HALL_3, INPUT );

  interrupts();
  attachInterrupt( digitalPinToInterrupt( HALL_1 ), isrHallSeq, CHANGE );
  attachInterrupt( digitalPinToInterrupt( HALL_2 ), isrHallSeq, CHANGE );
  attachInterrupt( digitalPinToInterrupt( HALL_3 ), isrHallSeq, CHANGE );
}

uint64_t prevmillis;

void loop()
{
  uint64_t currmillis = millis();
  uint64_t dt = currmillis - prevmillis;
  uint16_t motorfreq;

#if DEBUG
  Serial.print(analogRead(IS_1));
  Serial.print("\t");
  Serial.print(analogRead(IS_2));
  Serial.print("\t");
  Serial.println(analogRead(IS_3));
  Serial.println(HALLSTATE);
  Serial.print(one);
  Serial.print(two);
  Serial.println(three);
  Serial.println("################");
  delay(100);
#endif

  if( currmillis < 8000 )
    if( dt > 62 ) // 1/16 s = 62.5 ms
    {
      motorfreq = revcount >> 4; // divide by 16
      revcount = 0;
    }
  else
    pwm = 0;

  prevmillis = currmillis;
}
