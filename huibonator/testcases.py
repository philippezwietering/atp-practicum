from Effector import Effector
from Sensor import Sensor, TemperatureSensor, LevelSensor, ColourSensor
from Constants import *
from time import sleep
from Simulator import Plant, Simulator
import Simproxy
import unittest

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
    pass

class PumpAndDistanceTests(unittest.TestCase):

    def testdistance(self):
        sim = Simulator(plant, Controller(), True)

        sample1 = afstand.read_mm()

        wpump.set(1)
        spump.set(1)


        for range(20):
            sim.update()

        wpump.set(0)
        spump.set(0)

        self.failUnless(sample1 < afstand.read_mm())

unittest.main()
