#ifndef FP_H_
#define FP_H_

#include "avrfix.h"

// typedef _Accum fp_t;
typedef _sAccum fp_t;

// #define fpmul(a,b) mulk(a,b)
// #define fpdiv(a,b) divk(a,b)
#define fpmul(a,b) smulsk(a,b)
#define fpdiv(a,b) sdivsk(a,b)

#endif
