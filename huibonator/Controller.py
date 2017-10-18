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
from time import sleep
from Simulator import Plant, Simulator
import Simproxy

plant = Plant()
hw = Simproxy.lemonator(plant)

class Controller:
    def __init__(self, lemonator):
        self.lemonator = lemonator
        self.state = "Waiting"
        sleep(5)
        for x in "Hello\n":
            self.lemonator.lcd.putc(x)

    def update(self):
        if ("A" == self.lemonator.keypad.getc()) and (self.lemonator.reflex.get()):
            self.lemonator.sirup_valve.set(0)
            self.lemonator.sirup_pump.set(1)
            self.state = "Pumping"
            for x in "Pumping syrup\n":
                self.lemonator.lcd.putc(x)

        if self.lemonator.distance.read_mm() < 80 or not self.lemonator.reflex.get() and self.state == "Pumping":
            self.lemonator.sirup_pump.set(0)
            self.lemonator.sirup_valve.set(1)
            self.lemonator.water_valve.set(0)
            self.lemonator.water_pump.set(1)
            for x in "Pumping water\n":
                self.lemonator.lcd.putc(x)

        if self.lemonator.distance.read_mm() < 44 or not self.lemonator.reflex.get() and self.state == "Pumping":
            self.lemonator.water_pump.set(0)
            self.lemonator.water_valve.set(1)
            self.state == "Waiting"

        for x in "Finished!\n":
            self.lemonator.lcd.putc(x)



sim = Simulator(plant, Controller(hw), True)
sim.run()
