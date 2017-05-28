#define DEBUG 1

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

uint8_t FLAG = 1;
/*
  A - Orange
  B - Blue
  C - Yellow
*/

#define setPWMA( value ) { bitSet( TCCR1A, COM1A1 );\
                           OCR1A = (uint8_t) value; }
#define setPWMB( value ) { bitSet( TCCR1A, COM1B1 );\
                           OCR1B = (uint8_t) value; }
#define setPWMC( value ) { bitSet( TCCR1A, COM1C1 );\
                           OCR1C = (uint8_t) value; }
#define stopPWMA()       ( bitClear( TCCR1A, COM1A1 ) )
#define stopPWMB()       ( bitClear( TCCR1A, COM1B1 ) )
#define stopPWMC()       ( bitClear( TCCR1A, COM1C1 ) )


volatile uint8_t pwm = 0;
volatile uint16_t revcount = 0;


void isrHallSeq()
{
  uint8_t hallstate = digitalRead( HALL_3 ) |
    ( digitalRead( HALL_2 ) << 1 ) |
    ( digitalRead( HALL_1 ) << 2 );

  revcount++;

  switch( hallstate )
  {
  case 1: // A->C
    digitalWrite( INH_B, LOW );
    stopPWMB();
    stopPWMC();
    digitalWrite( INH_C, HIGH );
    setPWMA( pwm );
    digitalWrite( INH_A, HIGH );
    break;
  case 2: // C->B
    digitalWrite( INH_A, LOW );
    stopPWMA();
    stopPWMB();
    digitalWrite( INH_B, HIGH );
    setPWMC( pwm );
    digitalWrite( INH_C, HIGH );
    break;
  case 3: // A->B
    digitalWrite( INH_C, LOW );
    stopPWMC();
    stopPWMB();
    digitalWrite( INH_B, HIGH );
    setPWMA( pwm );
    digitalWrite( INH_A, HIGH );
    break;
  case 4: // B->A
    digitalWrite( INH_C, LOW );
    stopPWMC();
    stopPWMA();
    digitalWrite( INH_A, HIGH );
    setPWMB( pwm );
    digitalWrite( INH_B, HIGH );
    break;
  case 5: // B->C
    digitalWrite( INH_A, LOW );
    stopPWMA();
    stopPWMC();
    digitalWrite( INH_C, HIGH );
    setPWMB( pwm );
    digitalWrite( INH_B, HIGH );
    break;
  case 6: // C->A
    digitalWrite( INH_B, LOW );
    stopPWMB();
    stopPWMA();
    digitalWrite( INH_A, HIGH );
    setPWMC( pwm );
    digitalWrite( INH_C, HIGH );
    break;
  }
}


void setup()
{
  noInterrupts();

#if DEBUG
  Serial.begin( 57600 );
#endif

  pwm = 0;
  OCR1A = 0;
  OCR1B = 0;
  OCR1C = 0;

  // Disable all compare outputs, Fast PWM 8 bit
  TCCR1A = bit( WGM10 ); // Sec. 14.10.1, Table 14.2
  // Prescaler clock/8, Fast PWM 8 bit -> 7.8KHz PWM
  TCCR1B = bit( WGM12 ) | bit( CS11 ); // Sec. 14.10.3, Tables 14.4-5
  TCCR1C = 0; // Sec. 14.10.5

  // Set port B compare pins as output
  digitalWrite( IN_A, LOW );
  digitalWrite( IN_B, LOW );
  digitalWrite( IN_C, LOW );

  pinMode( IN_A, OUTPUT );
  pinMode( IN_B, OUTPUT );
  pinMode( IN_C, OUTPUT );

  digitalWrite( INH_A, LOW );
  digitalWrite( INH_B, LOW );
  digitalWrite( INH_C, LOW );

  pinMode( INH_A, OUTPUT );
  pinMode( INH_B, OUTPUT );
  pinMode( INH_C, OUTPUT );

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
  //Serial.print(analogRead(IS_A));
//  Serial.print("\t");
//  Serial.print(analogRead(IS_B));
//  Serial.print("\t");
//  Serial.println(analogRead(IS_C));
  //Serial.println(HALLSTATE);
  //Serial.print(one);
  //Serial.print(two);
  //Serial.println(three);
  //Serial.print(OCR1A);
  //Serial.print(" ");
  //Serial.println(TCNT1);
  
  //Serial.println("################");
  //delay(100);
#endif

  if( currmillis < 10000 )
  {
    pwm = 60;
    //Serial.println(dt);
    if( dt > 62 ) // 1/16 s = 62.5 ms
    {
      uint8_t OLDSREG = SREG;
      motorfreq = (revcount * 1000) / 12 / dt;
      SREG = OLDSREG;
      #if DEBUG
//      Serial.println(motorfreq);
      #endif
      //motorfreq = revcount >> 4; // divide by 16
      revcount = 0; 
      prevmillis = currmillis;
      SPDR = motorfreq;
      
    }
  }
  else{
    pwm = 0;
    if (FLAG == 1){
      Serial.print("end");
    } 
    FLAG = 0;
  }
}
