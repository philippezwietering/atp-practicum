// ==========================================================================
//
// blink the LED on an Arduino Due
//
// (c) Wouter van Ooijen (wouter@voti.nl) 2017
//
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE_1_0.txt or copy at 
// http://www.boost.org/LICENSE_1_0.txt) 
//
// ==========================================================================

//! [[blink example]]
#include "hwlib-arduino-due.hpp"

int main( void ){

   // kill the watchdog (ATSAM3X8E specific)
   WDT->WDT_MR = WDT_MR_WDDIS;
   
   auto led = hwlib::target::pin_out( 1, 27 );
   hwlib::blink( led );
}
//! [[blink example]]
