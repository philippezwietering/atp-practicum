import lemonator
import Controller
import time

print( "Python interface demo running" )
hw = lemonator.lemonator( 24 )
contr = Controller.controller(hw)
led = hw.led_yellow
while 1:
   # led.set( 1 )
   # time.sleep( 0.5 )
   # led.set( 0 )
   # time.sleep( 0.5 )

   contr.update()
