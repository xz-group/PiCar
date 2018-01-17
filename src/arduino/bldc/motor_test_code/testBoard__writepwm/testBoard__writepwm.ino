// TEST D9,D10,D11 PWM

//#define INH_A A2 //Yellow
//#define INH_B A1 //Blue
//#define INH_C A0 //Orange

#define IN_A 9  //Yellow  
#define IN_B 10 //Blue
#define IN_C 11  //Orange

//EANBLE D9,D10,D11 ON TIMER 1
#define setPWMA(value) { bitSet(TCCR1A, COM1A1);OCR1A = (uint8_t)value;}
#define setPWMB(value) { bitSet(TCCR1A, COM1B1);OCR1B = (uint8_t)value;}
#define setPWMC(value) { bitSet(TCCR1A, COM1C1);OCR1C = (uint8_t)value;}

void setup()
{
  
  OCR1A = 0;
  OCR1B = 0;
  OCR1C = 0;
  TCCR1A = bit(WGM10);
  TCCR1B = bit(WGM12)|bit(CS11);//7.8KHZ
  TCCR1C = 0;
  
  DDRF |= 0B11100000;//INHIBIT AS OUTPUT set A0, A1, A2 as output
  
  pinMode( IN_A, OUTPUT );
  pinMode( IN_B, OUTPUT );
  pinMode( IN_C, OUTPUT );
  
  //inhibit mode
  PORTF = 0B00011111;//low
  
  delay(500);

  setPWMA(10);
  setPWMB(100);
  setPWMC(200);
}


void loop()
{

}

