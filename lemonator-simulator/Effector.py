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
    def update(self) -> None:
        if self._vessel != None:
            if self._value:
                self._vessel._pressure = min(self._vessel._pressure + 100 / pressureRampUp, 100)
                self._vessel._pumping = True
            else:
                self._vessel._pressure = max(self._vessel._pressure - 100 / pressureRampDown, 0)
                self._vessel._pumping = False


class Valve(Effector):
    def update(self):
        if self._value and self._vessel != None:
            self._vessel._pressure = 0


class Heater(Effector):
    def update(self) -> None:
        if self._value:
            if isinstance(self._vessel, MixtureVessel):
                self._vessel.heat(True)
        elif isinstance(self._vessel, MixtureVessel):
            self._vessel.heat(False)

class Led(Effector):
    def toggle(self):
        if self.isOn():
            self.switchOff()
        else:
            self.switchOn()

class LCD(Effector):
    def put(self, char):
        print(char, end='', flush=True)
