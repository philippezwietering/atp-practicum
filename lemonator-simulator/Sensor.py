# uncompyle6 version 2.12.0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Nov 17 2016, 17:05:23)
# [GCC 5.4.0 20160609]
# Embedded file name: .\Sensor.py
# Compiled at: 2017-08-29 16:33:33
# Size of source mod 2**32: 1866 bytes
from Vessel import Vessel, MixtureVessel
from math import pi
from Constants import *

class Sensor:

    def __init__(self, vessel: Vessel):
        self._vessel = vessel
        self._value = 0
        self._unitOfMeasure = ''

    def update(self) -> None:
        pass

    def readValue(self) -> float:
        return round(self._value, 2)

    def measure(self) -> str:
        return str(self._convertToValue()) + self._unitOfMeasure

    def _convertToValue(self) -> float:
        return round(self._value, 2)


class ColourSensor(Sensor):

    def __init__(self, vessel: Vessel):
        Sensor.__init__(self, vessel)
        self._unitOfMeasure = '%'

    def update(self) -> None:
        if type(self._vessel) != None:
            colour = self._vessel.getColour()
            self._value = colour * colourConversion

    def _convertToValue(self) -> float:
        return round(self._value / colourConversion, 2)


class TemperatureSensor(Sensor):

    def __init__(self, vessel: Vessel):
        Sensor.__init__(self, vessel)
        self._unitOfMeasure = '°C'

    def update(self) -> None:
        if type(self._vessel) != None:
            temperature = self._vessel.getTemperature()
            self._value = temperature * tempConversion

    def _convertToValue(self) -> float:
        return round(self._value / tempConversion, 2)


class LevelSensor(Sensor):

    def __init__(self, vessel: Vessel):
        Sensor.__init__(self, vessel)
        self._unitOfMeasure = 'ml'

    def update(self) -> None:
        if type(self._vessel) != None:
            level = self._vessel.getFluidAmount()
            height = level / pi / 10 / 10
            self._value = height * levelConversion

    def _convertToValue(self) -> float:
        return round(self._value / levelConversion * pi * 10 * 10, 2)

class ReflexSeonsor(Sensor):
    def __init__(self, vessel: MixtureVessel):
        Sensor.__init__(self, vessel)

    def update(self):
        self._value = self._vessel.getPresence()

class keypadSensor(Sensor):

    def __init__(self):
        Sensor.__init__(self, None)
        self._unitOfMeasure = ''
        self._value = 0
        self._read = ''

    def pressKey(self, c):
        if c not in [x for x in "0123456789ABCD*#"]:
            return
        self._read = c

    def getc(self):
        retval = self._read
        self._read = ''
        return retval
