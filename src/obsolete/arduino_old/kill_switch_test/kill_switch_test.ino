volatile uint16_t rising;
volatile int32_t diff;
volatile uint8_t input_high = 0;

ISR(TIMER1_CAPT_vect) {
  int32_t timer = (int32_t) TCNT1;
  diff = timer;
  if( input_high )
  {
    bitClear(TCCR1B, 6);
//    rising = timer;
    input_high = 0;
  }
  else
  {
    bitSet(TCCR1B, 6);
//    diff = rising;
//    if( timer < rising )
//      //diff = 0;
//      diff = ( rising );
//    else
//      diff = timer - rising;
    input_high = 1;
  }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(8,INPUT);
  
  bitSet(TCCR1B, 6);
  // bitSet(TCCR1B, 7);
  bitSet(TIMSK1, 5);

  input_high = 1;
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println( diff );
//  Serial.println(bitRead(TCCR1B,6));
}
