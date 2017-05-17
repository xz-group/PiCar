/**********************************************************
 SPI_Raspi_Arduino
   Configures an Raspberry Pi as an SPI master and
   demonstrates a basic bidirectional communication scheme
   with an Arduino slave.  The Raspberry Pi transmits
   commands to perform addition and subtraction on a pair
   of integers and the Ardunio returns the result

Compile String:
g++ -o SPI_Raspi_Arduino SPI_Raspi_Arduino.cpp
***********************************************************/

#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>
#include <fcntl.h>
#include <iostream>
#include <cstring>


using namespace std;


/**********************************************************
Housekeeping variables
***********************************************************/
int results;
int fd;

/**********************************************************
Declare Functions
***********************************************************/

int spiTxRx(unsigned char txDat);
int sendCommand(char i, int j, int k);

/**********************************************************
Main
***********************************************************/

int main (void)
{

/**********************************************************
Setup SPI
Open file spidev0.0 (chip enable 0) for read/write access
with the file descriptor "fd"
Configure transfer speed (1MkHz)
***********************************************************/

   fd = open("/dev/spidev0.0", O_RDWR);

   unsigned int speed = 1000000;
   ioctl (fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);

/**********************************************************
An endless loop that repeatedly sends the demonstration
commands to the Arduino and displays the results
***********************************************************/

   while (1)
   {

      results = sendCommand('a', 60, 655);



      //results = sendCommand('s', 1000, 250);



      sleep(1);
      
      results = sendCommand('a', 120, 655);



      sleep(1);

     }

}

/**********************************************************
spiTxRx
 Transmits one byte via the SPI device, and returns one byte
 as the result.

 Establishes a data structure, spi_ioc_transfer as defined
 by spidev.h and loads the various members to pass the data
 and configuration parameters to the SPI device via IOCTL

 Local variables txDat and rxDat are defined and passed by
 reference.  
***********************************************************/

int spiTxRx(unsigned char txDat)
{
 
  unsigned char rxDat;

  struct spi_ioc_transfer spi;

  memset (&spi, 0, sizeof (spi));

  spi.tx_buf        = (unsigned long)&txDat;
  spi.rx_buf        = (unsigned long)&rxDat;
  spi.len           = 1;

  ioctl (fd, SPI_IOC_MESSAGE(1), &spi);

  return rxDat;
}


/**********************************************************
sendCommand
 Demonstration of a protocol that uses the spiTxRx function
 to send a formatted command sequence/packet to the Arduino
 one byte at and capture the results
***********************************************************/


int sendCommand(char command, int j, int k)
{

unsigned char resultByte;
bool ack;

/**********************************************************
Unions allow variables to occupy the same memory space
a convenient way to move back and forth between 8-bit and
16-bit values etc.

Here three unions are declared: two for parameters to be 
passed in commands to the Arduino and one to receive
the results
***********************************************************/

union p1Buffer_T       
{
  int p1Int;
  unsigned char  p1Char [2];
} p1Buffer;

union p2Buffer_T      
{
  int p2Int;
  unsigned char  p2Char [2];
} p2Buffer;

union resultBuffer_T     
{
  int resultInt;
  unsigned char  resultChar [2];
} resultBuffer;


  p1Buffer.p1Int = j;
  p2Buffer.p2Int = k;
  resultBuffer.resultInt = 0;

/**********************************************************
An initial handshake sequence sends a one byte start code
('c') and loops endlessly until it receives the one byte 
acknowledgment code ('a') and sets the ack flag to true.
(Note that the loop also sends the command byte while 
still in handshake sequence to avoid wasting a transmit
cycle.)
***********************************************************/

  do
  {
    ack = false;

    spiTxRx('c');
    usleep (10);


    resultByte = spiTxRx(command);
    if (resultByte == 'a')
    {
      ack = true;
    }
    usleep (10);  

   }
  while (ack == false);

/**********************************************************
Send the parameters one byte at a time.
***********************************************************/

  spiTxRx(p1Buffer.p1Char[0]);
  usleep (10);


  spiTxRx(p1Buffer.p1Char[1]);
  usleep (10);


  spiTxRx(p2Buffer.p2Char[0]);
  usleep (10);


  spiTxRx(p2Buffer.p2Char[1]);
  usleep (10);

/**********************************************************
Push two more zeros through so the Arduino can return the
results
***********************************************************/


  resultByte = spiTxRx(0);
  resultBuffer.resultChar[0] = resultByte;
  usleep (10);


  resultByte = spiTxRx(0);
  resultBuffer.resultChar[1] = resultByte;
  return resultBuffer.resultInt;

}
