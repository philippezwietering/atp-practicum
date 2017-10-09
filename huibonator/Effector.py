# uncompyle6 version 2.12.0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Nov 17 2016, 17:05:23) 
# [GCC 5.4.0 20160609]
# Embedded file name: .\Effector.py
# Compiled at: 2017-08-29 16:43:31
# Size of source mod 2**32: 1451 bytes
from Vessel import Vessel, MixtureVessel
from Constants import *

class Effector:

    def __init__(self, vessel: Vessel):
        self._vessel = vessel
        self._value = False

    def switchOn(self) -> None:
        self._value = True

    def switchOff(self) -> None:
        self._value = False

    def isOn(self) -> float:
        return self._value

    def update(self) -> None:
        pass


class Pump(Effector):

    def __init__(self, vessel: Vessel):
        Effector.__init__(self, vessel)
        self._pressure = 0

    def update(self) -> None:
        if self._pressure > 100 and self._vessel != None:
            self._vessel.flow()
        if self._value:
            self._pressure = min(self._pressure + 100 / pressureRampUp, 100)
            if self._pressure == 100:
                self._pressure = 200
        else:
            self._pressure = max(self._pressure - 100 / pressureRampDown, 0)


class Valve(Effector):
    pass


class Heater(Effector):

    def update(self) -> None:
        if self._value:
            if isinstance(self._vessel, MixtureVessel):
                self._vessel.heat(True)
        elif isinstance(self._vessel, MixtureVessel):
            self._vessel.heat(False)