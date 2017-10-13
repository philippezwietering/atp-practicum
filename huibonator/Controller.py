# uncompyle6 version 2.12.0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Nov 17 2016, 17:05:23)
# [GCC 5.4.0 20160609]
# Embedded file name: .\Controller.py
# Compiled at: 2017-08-29 16:53:26
# Size of source mod 2**32: 1554 bytes
from Effector import Effector
from Sensor import Sensor, TemperatureSensor, LevelSensor, ColourSensor
from Constants import *
from typing import Dict
from time import sleep
from Simulator import Plant, Simulator
import Simproxy

plant = Plant()
hw = Simproxy.lemonator(plant)
yled = hw.led_yellow
gled = hw.led_green
heat = hw.heater
wpump = hw.water_pump
spump = hw.sirup_pump
afstand = hw.distance
reflex = hw.reflex
lcd = hw.lcd

class Controller:

    def __init__(self):
        self.bool = True


    def update(self) -> None:
        # if not self._Controller__effectors['heater'].isOn():
        #     if self._Controller__sensors['temp'].readValue() + tempReaction < tempSetPoint:
        #         self._Controller__effectors['heater'].switchOn()
        # elif self._Controller__sensors['temp'].readValue() + tempReaction > tempSetPoint:
        #     self._Controller__effectors['heater'].switchOff()
        # if self._Controller__sensors['level'].readValue() + levelReaction < levelSetPoint:
        #     if self._Controller__sensors['color'].readValue() < colourSetPoint:
        #         self._Controller__effectors['pumpB'].switchOn()
        #     else:
        #         self._Controller__effectors['pumpA'].switchOn()
        # elif self._Controller__sensors['level'].readValue() + levelReaction > levelSetPoint:
        #     self._Controller__effectors['pumpA'].switchOff()
        #     self._Controller__effectors['pumpB'].switchOff()

        if self.bool:
            yled.set(0)
            gled.set(0)
            heat.set(0)
            wpump.set(0)
            spump.set(0)
            self.bool = False
        else:
            yled.set(1)
            gled.set(1)
            heat.set(1)
            wpump.set(1)
            spump.set(1)
            self.bool = True

        lcd.putc('a')
        lcd.putc('b')

        #/print(afstand.read_mm())
        #print(reflex.get())



sim = Simulator(plant, Controller(), True)
sim.run()
