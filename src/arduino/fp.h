#ifndef FP_H_
#define FP_H_

#include "avrfix.h"

// typedef _Accum fp_t;
typedef _sAccum fp_t;

// #define fpmul(a,b) mulk(a,b)
// #define fpdiv(a,b) divk(a,b)
#define fpmul(a,b) smulsk(a,b)
#define fpdiv(a,b) sdivsk(a,b)

// #define itofp(i) itok(i)
// #define fptoi(k) ktoi(k)
// #define ftofp(f) ftok(f)
// #define fptof(k) ktod(k)
#define itofp(i) itosk(i)
#define fptoi(k) sktoi(k)
#define ftofp(f) ftosk(f)
#define fptof(k) sktof(k)

#endif
