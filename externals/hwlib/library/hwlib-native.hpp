// ==========================================================================
//
// File      : hwlib-natuve.hpp
// Part of   : C++ hwlib library for close-to-the-hardware OO programming
// Copyright : wouter@voti.nl 2017
//
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
//
// ==========================================================================

// this file contains Doxygen lines
/// @file

#ifndef HWLIB_NATIVE_H
#define HWLIB_NATIVE_H

#include "hwlib-all.hpp"
#include <chrono>

namespace hwlib {

#ifdef HWLIB_ONCE

uint64_t now_ticks(){
    std::chrono::milliseconds ms = std::chrono::duration_cast< std::chrono::milliseconds >(std::chrono::system_clock::now().time_since_epoch());
    return ms.count();
}

uint64_t ticks_per_us(){
   return 1;
}

uint64_t now_us(){
   return now_ticks() / ticks_per_us();
}

void wait_us_busy( int_fast32_t n ){
   auto end = now_us() + n;
   while( now_us() < end ){}
}

/*

void wait_ns( int_fast32_t n ){
   wait_us( n / 1'000 );
}

void wait_us( int_fast32_t n ){

}

void wait_ms( int_fast32_t n ){
   wait_us( n * 1'000 );
}

uint_fast64_t now_us(){
   return 0;
}

*/

void uart_putc( char c ){}

char uart_getc(){
   return '?';
}

bool HWLIB_WEAK uart_char_available(){
   return 0;
}



#endif // #ifdef HBLIB_ONCE

}; // namespace hwlib

#endif // HWLIB_NATIVE_H
