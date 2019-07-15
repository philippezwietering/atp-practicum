# uncompyle6 version 3.3.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: .\Effector.py
# Size of source mod 2**32: 3451 bytes
from Vessel import Vessel, MixtureVessel
from Constants import *
from typing import Tuple

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
        if self._pressure > 100:
            if self._vessel != None:
                self._vessel.flow()
            if self._value:
                self._pressure = min(self._pressure + 100 / pressureRampUp, 100)
                if self._pressure == 100:
                    self._pressure = 200
                else:
                    self._pressure = max(self._pressure - 100 / pressureRampDown, 0)


class Valve(Effector):

    def setPump(self, pump: Pump) -> None:
        self._Valve__pump = pump

    def update(self) -> None:
        if self._value:
            self._Valve__pump._pressure = 0
            self._value = False


class Heater(Effector):

    def update(self) -> None:
        if self._value:
            if isinstance(self._vessel, MixtureVessel):
                self._vessel.heat(True)
            elif isinstance(self._vessel, MixtureVessel):
                self._vessel.heat(False)


class Led(Effector):

    def __init__(self, colour: Tuple[(int, int, int)]) -> None:
        Effector.__init__(self, None)
        self._Led__colour = colour

    def getColour(self):
        return self._Led__colour

    def toggle(self):
        if self._value:
            self.switchOff()
        else:
            self.switchOn()


class LCD(Effector):

    def __init__(self) -> None:
        Effector.__init__(self, None)
        self._LCD__lines = [[], [], [], []]
        self._LCD__cursor = (0, 0)

    def getLines(self) -> str:
        return map(lambda x: ''.join(x), self._LCD__lines)

    def pushString(self, s: str) -> None:
        for i in range(len(s)):
            c = s[i]
            if c == '\x0c':
                self.clear()
                self._LCD__cursor = (0, 0)
            elif c == '\n':
                self._LCD__cursor = (
                 0, (self._LCD__cursor[1] + 1) % 4)
            elif c == '\r':
                self._LCD__cursor = (
                 0, self._LCD__cursor[1])
            elif c == '\t':
                if i + 4 >= len(s):
                    print('ERROR in parsing String input', s)
                x = int(s[(i + 1)] + s[(i + 2)])
                y = int(s[(i + 3)] + s[(i + 4)])
                self._LCD__cursor = (x, y)
            else:
                self.put(c)

    def clear(self) -> None:
        self._LCD__lines = []
        for _ in range(4):
            self._LCD__lines.append(list('                    '))

    def put(self, s: str) -> None:
        x, y = self._LCD__cursor
        if y > 4:
            print('ERROR, trying to put a character on none existing line', y)
            return
        line = self._LCD__lines[y]
        if x > len(line):
            print('ERROR, trying to put a character on a none existing position', x)
            return
        line[x] = s
        if x == 20:
            y = (y + 1) % 20
        x = (x + 1) % 20
        self._LCD__cursor = (x, y)