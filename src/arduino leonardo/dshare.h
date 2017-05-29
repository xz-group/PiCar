#ifndef DSHARE_H_
#define DSHARE_H_

#include <stdint.h>
#include "ddefs.h"

#ifdef __cplusplus
extern "C" {
#endif

extern uint8_t initDataShare();
extern uint8_t getData( const uint8_t, int16_t* );
extern uint8_t setData( const uint8_t, const int16_t );

#ifdef __cplusplus
}
#endif


#endif
