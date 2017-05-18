#ifndef PID_H_
#define PID_H_

#include "avrfix.h"

#define PID_OK 0
#define PID_INVALID_PARAM 1
#define PID_INVALID_STRUCT 2

typedef struct
{
  enum { P, PI, PID, PD, NA } mode = NA;
  _sAccum state;
  _sAccum errm;
  _sAccum errmm;
  _sAccum Kp;
  _sAccum Ti;
  _sAccum Td;
} pid;


#ifdef __cplusplus
extern "C"{
#endif

uint8_t initPID( pid * );
uint8_t setPIDParams( pid *, _sAccum, _sAccum, _sAccum );
uint8_t updatePID( pid *, _sAccum, _sAccum );

#ifdef __cplusplus
}
#endif

#endif
