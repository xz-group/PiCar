#ifndef FP_H_
#define FP_H_

#include "avrfix.h"

// set resolution: SK=7.8 (16bit), K=15.16 (32bit)
#define FPSK 1
#define FPK 0

#if FPSK && FPK
#error FPSK and FPK are mutually exclusive!
#endif

#ifdef FPSK
typedef _sAccum fp_t;

#define fpmul(a,b) smulsk(a,b)
#define fpdiv(a,b) sdivsk(a,b)

#define itofp(i) itosk(i)
#define fptoi(k) sktoi(k)
#define ftofp(f) ftosk(f)
#define fptof(k) sktof(k)

#elif FPK
typedef _Accum fp_t;

#define fpmul(a,b) mulk(a,b)
#define fpdiv(a,b) divk(a,b)

#define itofp(i) itok(i)
#define fptoi(k) ktoi(k)
#define ftofp(f) ftok(f)
#define fptof(k) ktod(k)

#endif

#endif
