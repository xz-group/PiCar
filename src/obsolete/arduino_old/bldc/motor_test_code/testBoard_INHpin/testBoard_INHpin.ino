

#define INH_A A2 //Yellow
#define INH_B A1 //Blue
#define INH_C A0 //Orange

void setup()
{
  PORTF  &= B00011111;
  PORTF  |= B00000000;
}

void loop()
{

    PORTF  = B10111111;  
    delay(1);
    PORTF  = B11011111;  
    delay(1);
    PORTF  = B01111111; 
    delay(1);
}

