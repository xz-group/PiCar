/**********************************************************
 SPI_Hello_Arduino
   Configures an Raspberry Pi as an SPI master and  
   demonstrates bidirectional communication with an 
   Arduino Slave by repeatedly sending the text
   "Hello Arduino" and receiving a response
   
Compile String:
g++ -o SPI_Hello_Arduino SPI_Hello_Arduino.cpp
***********************************************************/

#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>
#include <fcntl.h>
#include <cstring>
#include <iostream>

using namespace std;


/**********************************************************
Declare Global Variables
***********************************************************/

int fd;
unsigned char hello[] = {'H','e','l','l','o',' ',
                           'A','r','d','u','i','n','o'};
unsigned char result;

/**********************************************************
Declare Functions
***********************************************************/

int spiTxRx(unsigned char txDat);


/**********************************************************
Main
  Setup SPI
    Open file spidev0.0 (chip enable 0) for read/write 
      access with the file descriptor "fd"
    Configure transfer speed (1MkHz)
  Start an endless loop that repeatedly sends the characters
    in the hello[] array to the Ardiuno and displays
    the returned bytes
***********************************************************/

int main (void)
{


   fd = open("/dev/spidev0.0", O_RDWR);

   unsigned int speed = 100000;
   ioctl (fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);

   while (1)
   {

      for (int i = 0; i < sizeof(hello); i++)
      {
         result = spiTxRx(hello[i]);
         cout << result;
         usleep (10);
      }

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
