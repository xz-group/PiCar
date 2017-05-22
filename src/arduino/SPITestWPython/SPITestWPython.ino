int pwm;
int servo;
byte marker;
unsigned char dat;
byte receive;

void setup() {
  // put your setup code here, to run once:
    //  SPI.begin();
  SPCR |= _BV(SPE);
  Serial.begin(115200);
//  pinMode(10,INPUT);
//  digitalWrite(10,LOW);
  pinMode(MISO, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:   
    if((SPSR & (1 << SPIF)) != 0)
    { 
      spiHandler();
   }
}

void spiHandler()
{
  switch (marker)
  {
  case 0:
    dat = SPDR;
    receive = dat;
    if (dat == 1)
    {
      SPDR = 1;
      marker++;
    }
    else if (dat == 2) {
      SPDR = 2;
      marker++; 
    }
    else {
      Serial.println("dat is wrong 1");
    }
    Serial.println(dat);
    break;    
  case 1:
    if(receive == 1) {
      pwm = SPDR;
      SPDR = pwm;
      Serial.print("pwm: ");
      Serial.println(pwm);
      marker = 0;
    }
    else if (receive == 2) {
      servo = SPDR;
      SPDR = servo;
      Serial.print("servo: ");
      Serial.println(servo);
      marker = 0;
    }
    else {
      Serial.println("dat is wrong 2");
    }
    break;
  }
//  case 2:
//    receiveBuffer[marker-1] = SPDR;
//    Serial.println(receiveBuffer[marker-1]);
//    marker++;
//    break;
//  case 3:
//    receiveBuffer[marker-1] = SPDR;
//    Serial.println(receiveBuffer[marker-1]);
//    marker++;
//    break;
//  case 4:
//    receiveBuffer[marker-1] = SPDR;
//    Serial.println(receiveBuffer[marker-1]);
//    marker++;
//    break;
//  case 5:
//    receiveBuffer[marker-1] = SPDR;
//    Serial.println(receiveBuffer[marker-1]);
//    marker++;
//    executeCommand();
//    SPDR = resultBuffer.resultChar[0];    
//    break;    
//  case 6:
//    marker++;
//    Serial.println(receiveBuffer[marker-1]);
//    SPDR = resultBuffer.resultChar[1]; 
//    break;   
//  case 7:
//    dat = SPDR;
//    Serial.println(receiveBuffer[marker-1]);
//    marker=0;
//  }

}

/***************************************************************  
 executeCommand
   When the complete 5 byte command sequence has been received
   reconstitute the byte variables from the receiveBuffer
   into integers, parse the command (add or subtract) and perform
   the indicated operation - the result will be in resultBuffer
****************************************************************/

  
//void executeCommand(void)
//{
//
//
//
// p1Buffer.p1Char[0]=receiveBuffer[1];
// p1Buffer.p1Char[1]=receiveBuffer[2];
// p2Buffer.p2Char[0]=receiveBuffer[3];
// p2Buffer.p2Char[1]=receiveBuffer[4];
// 
//  resultBuffer.resultInt = 1;
//
//
//} 
