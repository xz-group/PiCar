// INPUT - DESIRED RPM
// OUTPUT - PWM

#include <stdint.h>
//#include "fp.h"
//#include "signalproc.h"
#include "ddefs.h"
#include "dshare.h"
#include "speed_control.h"

uint16_t PID = 1; // temporary constant
uint16_t RPM_curr;
uint16_t PWM_new;
uint16_t RPM_err;

uint16_t toPWM(uint16_t RPM_des)
{
  if ( getData( BLDC_HALL_SPEED, &RPM_curr ) == DSHARE_OK );
  
  RPM_err = RPM_des - RPM_curr;
  PWM_new = PID*RPM_err;

  // Saturation between 0 and 255
  if(PWM_new > 255)
    PWM_new = 255;
  else if(PWM_new < 0)
    PWM_new = 0;
    
  return PWM_new;
}

