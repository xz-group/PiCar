//test on PCB board
//PCB HALL SENSORS CONNECTED TO SS(D17),SCK(D15),MOSI(D16)


#define IN_A 9  //Yellow  
#define IN_B 10 //Blue
#define IN_C 11  //Orange

#define INH_A A2 //Yellow
#define INH_B A1 //Blue
#define INH_C A0 //Orange

#define HALL_1 17
#define HALL_2 15
#define HALL_3 16


//EANBLE D9,D10,D11 ON TIMER 1
#define setPWMA(value) { bitSet(TCCR1A, COM1A1);OCR1A = (uint8_t)value;}
#define setPWMB(value) { bitSet(TCCR1A, COM1B1);OCR1B = (uint8_t)value;}
#define setPWMC(value) { bitSet(TCCR1A, COM1C1);OCR1C = (uint8_t)value;}

#define stopPWMA()     { bitClear(TCCR1A,COM1A1);}
#define stopPWMB()     { bitClear(TCCR1A,COM1B1);}
#define stopPWMC()     { bitClear(TCCR1A,COM1C1);}

uint8_t pwm = 30;
uint16_t revcount = 0;
bool motorccw = 1;

void setup()
{

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

  OCR1A = 0;
  OCR1B = 0;
  OCR1C = 0;
  TCCR1A = bit(WGM10);
  TCCR1B = bit(WGM12)|bit(CS11);//7.8KHZ
  TCCR1C = 0;

  pinMode( IN_A, OUTPUT );
  pinMode( IN_B, OUTPUT );
  pinMode( IN_C, OUTPUT );

  DDRF |= 0B11100000;//SET AS OUTPUT

  pinMode( HALL_1, INPUT );
  pinMode( HALL_2, INPUT );
  pinMode( HALL_3, INPUT );

  digitalWrite( IN_A, LOW );
  digitalWrite( IN_B, LOW );
  digitalWrite( IN_C, LOW );
  PORTF  &= B00011111;
  PORTF  |= B00000000;
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
    PORTF  = B10101111;  
    stopPWMA();
    setPWMB(255);
    setPWMC(pwm);

    break;
  case 2: // B->C
    PORTF  = B11001111;  
    setPWMA(255);
    setPWMB(pwm);
    stopPWMC();
    break;
  case 3:// B->A
    PORTF  = B01101111; 
    stopPWMA();
    setPWMB(pwm);
    setPWMC(255);    
    break;
  case 4:      // A->B
    PORTF  = B01101111;  
    setPWMA(pwm);
    stopPWMB();
    setPWMC(255); 
    break;
  case 5:  //C->B
    PORTF  = B11001111;  
    setPWMA(255);
    stopPWMB();
    setPWMC(pwm);
    break;
  case 6: // A->C
    PORTF  = B10101111; 
    setPWMA(pwm);
    setPWMB(255);
    stopPWMC();
    break;
  }
}



