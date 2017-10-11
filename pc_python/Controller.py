# uncompyle6 version 2.12.0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Nov 17 2016, 17:05:23)
# [GCC 5.4.0 20160609]
# Embedded file name: .\Controller.py
# Compiled at: 2017-08-29 16:53:26
# Size of source mod 2**32: 1554 bytes
import lemonator

class controller:
    def __init__(self, lemonator):
        self.lemonator = lemonator
        self.lemonator.lcd.putc("H")
        self.lemonator.lcd.putc("e")
        self.lemonator.lcd.putc("l")
        self.lemonator.lcd.putc("l")
        self.lemonator.lcd.putc("o")

    def update(self):
        if "A" == lemonator.keypad.getc() and lemonator.reflex.get():
            lemonator.sirup_valve.set(1)
            lemonator.sirup_pump.set(1)
            while(1):
                if lemonator.distance.read_mm() < 110 or not lemonator.reflex.get():
                    lemonator.sirup_pump.set(0)
                    lemonator.sirup_valve.set(0)
                    break

            lemonator.water_valve.set(1)
            lemonator.water_pump.set(1)

            while(1):
                if lemonator.distance.read_mm() < 90 or not lemonator.reflex.get():
                    lemonator.water_pump.set(0)
                    lemonator.water_valve.set(0)
                    break
