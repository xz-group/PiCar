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

#define setPWMA( value ) { bitSet( TCCR1A, COM1A1 ); OCR1A = (uint8_t) value; digitalWrite( INH_A, HIGH ); }
#define setPWMB( value ) { bitSet( TCCR1A, COM1B1 ); OCR1B = (uint8_t) value; digitalWrite( INH_B, HIGH ); }
#define setPWMC( value ) { bitSet( TCCR1A, COM1C1 ); OCR1C = (uint8_t) value; digitalWrite( INH_C, HIGH ); }
#define stopPWMA()       { bitClear( TCCR1A, COM1A1 ); digitalWrite( INH_A, HIGH ); }
#define stopPWMB()       { bitClear( TCCR1A, COM1B1 ); digitalWrite( INH_B, HIGH ); }
#define stopPWMC()       { bitClear( TCCR1A, COM1C1 ); digitalWrite( INH_C, HIGH ); }
#define inhibitA()       { digitalWrite( INH_A, LOW ); }
#define inhibitB()       { digitalWrite( INH_B, LOW ); }
#define inhibitC()       { digitalWrite( INH_C, LOW ); }

volatile uint8_t pwm = 0;
volatile uint16_t revcount = 0;
volatile uint8_t motorccw = 1;

void isrHallSeq()
{
  uint8_t hallstate = digitalRead( HALL_3 ) |
    ( digitalRead( HALL_2 ) << 1 ) |
    ( digitalRead( HALL_1 ) << 2 );

  if( !motorccw )
    hallstate = ~hallstate;

  switch( hallstate )
  {
  case 1: // A->C
    inhibitB();
    stopPWMC();
    setPWMA( pwm );
    break;
  case 2: // C->B
    inhibitA();
    stopPWMB();
    setPWMC( pwm );
    break;
  case 3: // A->B
    inhibitC();
    stopPWMB();
    setPWMA( pwm );
    break;
  case 4: // B->A
    inhibitC();
    stopPWMA();
    setPWMB( pwm );
    break;
  case 5: // B->C
    inhibitA();
    stopPWMC();
    setPWMB( pwm );
    break;
  case 6: // C->A
    inhibitB();
    stopPWMA();
    setPWMC( pwm );
    break;
  }

  revcount++;
}


void setup()
{
#if DEBUG
  Serial.begin( 57600 );
#endif

  PWMsetup();
}

void loop()
{
  uint64_t currmillis = millis();
  PWMloop( currmillis );
}

void PWMsetup()
{
  noInterrupts();

  // Initialize global pwm sequence variables
  pwm = 0;
  motorccw = 1;
  revcount = 0;

  // Initialize compare modules. Sec. 14.10.9-11
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
  attachInterrupt( 2, isrHallSeq, CHANGE );
  attachInterrupt( 3, isrHallSeq, CHANGE );
  attachInterrupt( 4, isrHallSeq, CHANGE );
}

uint64_t prevmillis;
int32_t motorfreq = 0;
int32_t setpoint = 0;

void PWMloop( uint64_t currmillis )
{
  int32_t dt = currmillis - prevmillis;

  const int32_t accum_max = 20000;
  const int32_t Kp = 1;
  const int32_t Ti = 100;
  int32_t accum = 0;
  int32_t err = 0;
  int32_t mypwm = 0;

  // read setpoint from dshare
  // FIXME
  if( currmillis < 8000 )
    setpoint = 100;
  else
    setpoint = 0;

  // update motorfreq every 50ms
  if( dt > 50 )
  {
    // revcount increments 12 times per revolution, dt is in milliseconds => motorfreq in Hz
    noInterrupts();
    motorfreq = ( revcount * 1000 ) / dt / 12;
    revcount = 0;
    interrupts();
  

    // update pwm and motorccw using PI controller
    // FIXME
    err = setpoint - motorfreq;
    accum += err;
    if( accum > accum_max )
      accum = accum_max;
    else if( accum < -accum_max )
      accum = -accum_max;
  
    mypwm = Kp * ( err + ( accum * dt ) / Ti / 1000 );
    noInterrupts();
    if( mypwm < 0 )
    {
      mypwm = -mypwm;
      motorccw = 0;
    }
    else
      motorccw = 1;
    if( mypwm > 150 )
      pwm = 150;
    pwm = (uint8_t) mypwm;
    interrupts();
  
    // motor is not moving, but it should be, hence hand-trigger sequence switch
    if( setpoint != 0 && motorfreq == 0 )
    {
      noInterrupts();
      isrHallSeq();
      interrupts();
    }
  
    prevmillis = currmillis;
  }

#if DEBUG
  Serial.print( OCR1A );
#endif
}
