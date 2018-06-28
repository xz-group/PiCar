
//test on motor control board, write 6hz to 17(hall 1)
//read from 15 (hall 2) and write hall 2 state to 16(hall 3)
#define HALL_1 17
#define HALL_2 15
#define HALL_3 16


void setup()
{
  PWMsetup();

}

void loop()
{
digitalWrite(HALL_3,digitalRead(HALL_2));
digitalWrite(HALL_1,HIGH);
delay(10);
digitalWrite(HALL_1,LOW);
digitalWrite(HALL_3,digitalRead(HALL_2));
delay(10);
}

void PWMsetup()
{

  pinMode( HALL_1, OUTPUT );
  pinMode( HALL_2, INPUT );
  pinMode( HALL_3, OUTPUT );

}


