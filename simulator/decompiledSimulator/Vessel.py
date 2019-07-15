# uncompyle6 version 3.3.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: .\Vessel.py
# Size of source mod 2**32: 3130 bytes
from Constants import *

class Vessel:
    r"""' Class to describe containers of liquids;\n    two types:\n    - Storage vessels (generic type, attached with effectors, no sensors)\n    - Mixture vessel (has a tap, attached with only heater effector, all types of sensors).\n    '"""

    def __init__(self, amount=3000, colour=0, temperature=20, flowTo=None):
        self._amount = amount
        self._colour = colour
        self._temperature = temperature
        self._flowTo = flowTo
        self._presence = True

    def getFluidAmount(self):
        return self._amount

    def getColour(self):
        return self._colour

    def getTemperature(self):
        return self._temperature

    def getPresence(self):
        """Indicates presence of this vessel; only valid for the mixture vessel"""
        return self._presence

    def flow(self):
        """Moves one (measurement defined in Constants) amount of liquid to the vessel connected to this vessel"""
        amount = flowRate
        if flowRate > self._amount:
            amount = self._amount
        self._amount -= amount
        if self._flowTo != None:
            self._flowTo.flowIn(amount, self._colour)

    def flowIn(self, amount, colour):
        if not self._presence:
            print('ERROR', 'leaking liquid in a non-placed cup', type(self))
        elif self._amount + amount > liquidMax:
            print('ERROR', 'overflow occuring in', type(self))
        else:
            self._colour = (self._colour * self._amount + colour * amount) / (self._amount + amount)
            self._amount += amount

    def update(self):
        """Periodically called method to update the state of the vessel"""
        pass


class MixtureVessel(Vessel):
    r"""' Mixture extensions to Vessel\n    - heat(True/False) (increases water temperature)\n    '"""

    def __init__(self, amount=0, colour=0, temperature=20):
        Vessel.__init__(self, amount, colour, temperature)
        self._heat = False

    def heat(self, state=False):
        self._heat = state

    def setPresence(self, presence=None):
        """Places or removes the cup.
          Removing the cup is interpreted as emptying it.

          :param presence: sets presence to this value; if no value is given, it toggles presence"""
        if presence is None:
            presence = not self._presence
        self._presence = presence
        if presence is False:
            self._amount = 0
            self._colour = 0
            self._temperature = environmentTemp

    def update(self):
        """
        Updates the state of the mixture vessel depending on the state of the effectors.
        constants (flowRate, heatRate, temperatureDecay) defined in Constants.py
        """
        if self._heat:
            self._temperature += heatRate
        elif self._temperature > environmentTemp:
            self._temperature -= temperatureDecay