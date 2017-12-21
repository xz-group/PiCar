// test D15, D16, D17 as output pins

#define HALL_1 17
#define HALL_2 15
#define HALL_3 16


void setup()
{
  
  pinMode(HALL_1,OUTPUT);
  pinMode(HALL_2,OUTPUT);
  pinMode(HALL_3,OUTPUT);
  
  delay(500);

}


void loop()
{
  digitalWrite(HALL_1, HIGH);
  digitalWrite(HALL_2, HIGH);
  digitalWrite(HALL_3, HIGH);
  delay(100);

  digitalWrite(HALL_1, LOW);
  digitalWrite(HALL_2, LOW);
  digitalWrite(HALL_3, LOW);
  delay(100);
  
}

