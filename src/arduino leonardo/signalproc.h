#ifndef SIGNALPROC_H_
#define SIGNALPROC_H_

#include "fp.h"

#define PID_OK 0
#define PID_DISABLED 1

#define FILTER_OK 0

typedef struct
{
  _Bool enabled;
  fp_t state;
  fp_t errm;
  fp_t errmm;
  fp_t c;
  fp_t cm;
  fp_t cmm;
  fp_t max;
  fp_t min;
} pid;

typedef struct
{
  fp_t state;
  fp_t statem;
  fp_t statemm;
  fp_t datam;
  fp_t datamm;
  fp_t am;
  fp_t amm;
  fp_t b;
  fp_t bm;
  fp_t bmm;
} filter;

#ifdef FPSK
#define dtoafreq( omega, dt ) ( ktosk( tank( divk( mulk( omega, dt ), itok( 2 ) ) ) ) )
#elif FPK
#define dtoafreq( omega, dt ) ( tank( divk( mulk( omega, dt ), itok( 2 ) ) ) )
#endif

#ifdef __cplusplus
extern "C" {
#endif

uint8_t initPID( pid *z, fp_t, fp_t, fp_t, fp_t, fp_t, fp_t );
uint8_t updatePID( pid *, fp_t );
fp_t getPIDValue( pid * );
uint8_t disablePID( pid * );
uint8_t enablePID( pid * );

uint8_t initFilter( filter *, fp_t, fp_t );
uint8_t updateFilter( filter *, fp_t );
fp_t getFilterValue( filter * );

#ifdef __cplusplus
}
#endif

#endif
