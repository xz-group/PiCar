// INPUT - RPM, DIRECTION
// OUTPUT - PWM

#include <stdint.h>
#include "fp.h"
#include "signalproc.h"

uint8_t Kp = 1; // temporary constant
uint8_t PWM;
fp_t DIR;

uint8_t toPWM(fp_t RPM, int8_t DIRECTION)
{
  if(DIRECTION > 0)
    DIR = itofp( 1 );
  else
    DIR = itofp( -1 );
    
  PWM = fpmul(RPM, DIR);
  PWM = fpmul(PWM, Kp);
  return PWM;
}

