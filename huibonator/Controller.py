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
from Simproxy import *

class Controller:

    def __init__(self, proxy: SimProxy):



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

            if self.testbool:
                self.Yled.set(1)
            else:
                self.Yled.set(0)