#include <stdint.h>
#include "fp.h"
#include "signalproc.h"

// Forward Euler discretization of a PID. No deriv filter, no windup.
uint8_t initPID( pid *z, fp_t Kp, fp_t Ti, fp_t Td, fp_t dt, fp_t min, fp_t max )
{
  fp_t itmp = 0, dtmp = 0;
  fp_t one = itofp( 1 );

  z->state = 0;
  z->errm = 0;
  z->errmm = 0;

  if ( Kp == 0 )
  {
    z->enabled = 0;
    return PID_DISABLED;
  }

  if ( Ti != 0 )
    itmp = fpdiv( Ti, dt );

  if ( Td != 0 )
    dtmp = fpdiv( dt, Td );

  z->c = fpmul( Kp, one + itmp + dtmp );
  z->cm = fpmul( Kp, - one - dtmp - dtmp );
  z->cmm = fpmul( Kp, dtmp );

  z->max = max;
  z->min = min;
  z->enabled = 1;

  return PID_OK;
}

uint8_t updatePID( pid *z, fp_t err )
{
  // state += err * ( Kp + Kp * dt / Ti + Kp * Td / dt )
  //          + errm * ( - Kp - 2 * Kp * Td / dt ) + errmm * Kp * Td / dt

  if( !z->enabled )
    return PID_DISABLED;

  z->state += fpmul( z->c, err ) + fpmul( z->cm, z->errm ) + fpmul( z->cmm, z->errmm );
  z->errmm = z->errm;
  z->errm = err;

  if( z->state > z->max )
    z->state = z->max;
  else if( z->state < z->min )
    z->state = z->min;
}

fp_t getPIDValue( pid *z )
{
  if( !z->enabled )
    return 0;

  return z->state;
}

uint8_t disablePID( pid *z )
{
  z->state = 0;
  z->errm = 0;
  z->errmm = 0;
  z->enabled = 0;

  return PID_OK;
}

uint8_t enablePID( pid *z )
{
  z->enabled = 1;

  return PID_OK;
}

// Second order Butterworth filter with bilinear discretization
// shamelessly copied from https://www.robots.ox.ac.uk/~sjrob/Teaching/SP/l6.pdf, pg. 77
uint8_t initFilter( filter *z, fp_t omega, fp_t dt )
{
  fp_t one = itofp( 1 );
  fp_t two = itofp( 2 );
  fp_t xi = dtoafreq( omega, dt );
  fp_t xi2 = fpmul( xi, xi );
  fp_t sqrt2xi = fpmul( ftofp( 1.41421356237 ), xi );
  fp_t a = one + sqrt2xi + xi2;

  z->state = 0;
  z->statem = 0;
  z->statemm = 0;
  z->datam = 0;
  z->datamm = 0;

  z->am = fpdiv( xi2 - two, a );
  z->amm = fpdiv( one - sqrt2xi + xi2, a );
  z->b = fpdiv( xi2, a );
  z->bm = fpmul( two, z->b );
  z->bmm = z->b;

  return FILTER_OK;
}

uint8_t updateFilter( filter *z, fp_t data )
{
  z->state = - fpmul( z->am, z->statem ) - fpmul( z->amm, z->statemm )
             + fpmul( z->b, data ) + fpmul( z->bm, z->datam ) + fpmul( z->bmm, z->datamm );

  z->statemm = z->statem;
  z->statem = z->state;
  z->datamm = z->datam;
  z->datam = data;

  return FILTER_OK;
}

fp_t getFilterValue( filter *z )
{
  return z->state;
}

