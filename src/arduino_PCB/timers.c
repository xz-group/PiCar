#include <Arduino.h>

//FIX ME: make timers do stuff

void initTimers() {

  TCCR0A = 0;          // normal operation
  TCCR0B = bit(WGM02) | bit(CS00) | bit (CS02);   // pre-scaling//reserved mode//  clk/1024
  OCR0A =  100;       // compare A register value (1000 * clock speed)
  TIMSK0 = bit (OCIE0A);
//  // set up Timer 0
//  TCCR0A = 0;          // normal operation
//  TCCR0B = bit(WGM12) | bit(CS10) | bit (CS12);   // pre-scaling
//  OCR0A =  100;       // compare A register value (1000 * clock speed)
//  TIMSK0 = bit (OCIE1A);
//
//  // set up Timer 1
//  TCCR1A = 0;          // normal operation
//  TCCR1B = bit(WGM12) | bit(CS10) | bit (CS12);   // pre-scaling
//  OCR1A =  100;       // compare A register value (1000 * clock speed)
//  TIMSK1 = bit (OCIE1A);

//    // set up Timer 2
//  TCCR2A = 0;          // normal operation
//  TCCR2B = bit(WGM12) | bit(CS10) | bit (CS12);   // pre-scaling
//  OCR2A =  100;       // compare A register value (1000 * clock speed)
//  TIMSK2 = bit (OCIE2A);

//  // set up Timer 3
//  TCCR3A = 0;          // normal operation
//  TCCR3B = bit(WGM32) | bit(CS30) | bit (CS32);   // pre-scaling
//  OCR3A =  100;       // compare A register value (1000 * clock speed)
//  TIMSK3 = bit (ICIE3);
//
//  // set up Timer 4
//  TCCR4A = 0;          // normal operation
//  TCCR4B = bit(WGM12) | bit(CS10) | bit (CS12);   // pre-scaling
//  OCR4A =  999;       // compare A register value (1000 * clock speed)
//  TIMSK4 = bit (OCIE1A);
}

