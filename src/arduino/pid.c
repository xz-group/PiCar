#include <stdint.h>
#include "avrfix.h"
#include "pid.h"

uint8_t initPID( pid *z )
{
  z->state = 0;
  z->errm = 0;
  z->errmm = 0;

  return PID_OK;
}

uint8_t setPIDParams( pid *z, _sAccum Kp, _sAccum Ti, _sAccum Td )
{
  if( Kp == 0 )
    return PID_INVALID_PARAM;

  z->mode = P;
  z->Kp = Kp;
  
  if( Ti != 0 )
  {
    z->mode = PI;
    z->Ti = Ti;
  }

  if( Td != 0 )
  {
    if( z->mode == PI )
      z->mode = PID;
    else
      z->mode = PD;
    z->Td = Td;
  }

  return PID_OK;
}

uint8_t updatePID( pid *z, _sAccum err, _sAccum dt )
{
  _sAccum itmp = 0, dtmp = 0;

  if( z->mode == NA )
    return PID_INVALID_STRUCT;

  // state += Kp * ( err - errm ) + Kp * dt / Ti * err + Kp * Td / dt * ( err - 2 * errm + errmm )

  if( z->mode == PI || z->mode == PID )
    itmp = sdivsk( smulsk( dt, err ), z->Ti );
  
  if( z->mode == PD || z->mode == PID )
    dtmp = sdivsk( smulsk( z->Td, err - z->errm - z->errm + z->errmm ), dt );

  z->state += smulskD( z->Kp, err - z->errm + itmp + dtmp );
  z->errmm = z->errm;
  z->errm = err;
}

