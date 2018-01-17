// test A0,A1,A2 as output

//#define INH_A A2 //Yellow
//#define INH_B A1 //Blue
//#define INH_C A0 //Orange


void setup()
{
  
DDRF |= 0B11100000;//set as output
}


void loop()
{

  PORTF = 0B11111111;//high
  delay(500);
  PORTF = 0B00011111;//low
  delay(500);
}

