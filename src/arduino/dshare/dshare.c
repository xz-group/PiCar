#include "dshare.h"
#include "ddefs.h"

int16_t dataArr[ DSHARE_ARR_LENGTH ];

uint8_t initDataShare()
{
  return DSHARE_OK;
}

uint8_t getData( const uint8_t address, int16_t *data )
{
  if( address >= DSHARE_ARR_LENGTH )
    return DSHARE_INVALID;

  *data = dataArr[ address ];

  return DSHARE_OK;
}

uint8_t setData( const uint8_t address, int16_t data )
{
  if( address >= DSHARE_ARR_LENGTH )
    return DSHARE_INVALID;

  dataArr[ address ] = data;

  return DSHARE_OK;
}

