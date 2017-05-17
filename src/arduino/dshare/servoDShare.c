//
//  servoDShare.c
//  
//
//  Created by Matt Kollada on 5/17/17.
//
//

#include "servoDShare.h"
#include "dshare.h"
#include "ddefs.h"

Servo servo

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

ISR(TIMER1_COMPA_vect)
{
    static boolean state = false;
    state = !state;  // toggle
    digitalWrite (LED, state ? HIGH : LOW);
}

void setup() {
    
    // set up Timer 1
    TCCR1A = 0;          // normal operation
    TCCR1B = bit(WGM12) | bit(CS10) | bit (CS12);   // CTC, no pre-scaling
    OCR1A =  999;       // compare A register value (1000 * clock speed)
    TIMSK1 = bit (OCIE1A);             // interrupt on Compare A Match
}  // end of setup

void loop() { }
