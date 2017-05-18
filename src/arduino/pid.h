#ifndef PID_H_
#define PID_H_

#include "fp.h"

#define PID_OK 0
#define PID_INVALID_PARAM 1
#define PID_INVALID_STRUCT 2

enum pidMode_t { P, PI, PID, PD, NA };

typedef struct
{
  enum pidMode_t mode;
  fp_t state;
  fp_t errm;
  fp_t errmm;
  fp_t Kp;
  fp_t Ti;
  fp_t Td;
} pid;


#ifdef __cplusplus
extern "C" {
#endif

uint8_t initPID( pid * );
uint8_t setPIDParams( pid *, fp_t, fp_t, fp_t );
uint8_t updatePID( pid *, fp_t, fp_t );

#ifdef __cplusplus
}
#endif

#endif
