#ifndef DSHARE_H_
#define DSHARE_H_

#define INT16_LENGTH

uint8_t initDataShare();
uint8_t getData( const uint8_t address, int16_t *data );
uint8_t setData( const uint8_t address, const int16_t data );
