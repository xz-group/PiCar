/*
 * Script to read in values from remote control
 * to verify connection.
 *
 * pulseIn reads the length of a pulse that is either
 * HIGH or LOW (depending on the second argument).
 */

void setup(){
  Serial.begin(9600);
  // Initialize all pins to inputs
  for(int i = 2; i<=13; i++){
    pinMode(i, INPUT);
  } 
}

void loop(){
  // Read in pins 8 (throttle) and pin 9 (steer) 
  for(int i = 9; i<=9; i++){
    Serial.print("Pin ");
    Serial.print(i);
    Serial.print(" gave a pulse in reading of ");
    //Serial.println(map(pulseIn(i, HIGH), 1901, 959, 1000, 2000));
    Serial.println(map(pulseIn(i, HIGH), 1220, 1490, 1000, 2000));
  }
}
