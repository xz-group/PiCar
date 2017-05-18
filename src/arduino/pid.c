#include <stdint.h>
#include "fp.h"
#include "pid.h"

uint8_t initPID( pid *z )
{
  z->mode = NA;
  z->state = 0;
  z->errm = 0;
  z->errmm = 0;

  return PID_OK;
}

uint8_t setPIDParams( pid *z, fp_t Kp, fp_t Ti, fp_t Td )
{
  if ( Kp == 0 )
    return PID_INVALID_PARAM;

  z->mode = P;
  z->Kp = Kp;

  if ( Ti != 0 )
  {
    z->mode = PI;
    z->Ti = Ti;
  }

  if ( Td != 0 )
  {
    if ( z->mode == PI )
      z->mode = PID;
    else
      z->mode = PD;
    z->Td = Td;
  }

  return PID_OK;
}

uint8_t updatePID( pid *z, fp_t err, fp_t dt )
{
  fp_t itmp = 0, dtmp = 0;

  if ( z->mode == NA )
    return PID_INVALID_STRUCT;

  // state += Kp * ( err - errm ) + Kp * dt / Ti * err + Kp * Td / dt * ( err - 2 * errm + errmm )

  if ( z->mode == PI || z->mode == PID )
    itmp = fpdiv( fpmul( dt, err ), z->Ti );

  if ( z->mode == PD || z->mode == PID )
    dtmp = fpdiv( fpmul( z->Td, err - z->errm - z->errm + z->errmm ), dt );

  z->state += fpmul( z->Kp, err - z->errm + itmp + dtmp );
  z->errmm = z->errm;
  z->errm = err;
}

