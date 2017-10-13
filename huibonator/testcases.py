from Effector import Effector
from Sensor import Sensor, TemperatureSensor, LevelSensor, ColourSensor
from Constants import *
from time import sleep
from Simulator import Plant, Simulator
import Simproxy
import unittest

# yled = hw.led_yellow
# gled = hw.led_green
# heat = hw.heater
# wpump = hw.water_pump
# spump = hw.sirup_pump
# afstand = hw.distance
# reflex = hw.reflex
# lcd = hw.lcd

class Controller:

    def update(self):
        pass

class lemonatortests(unittest.TestCase):

    def testdistance(self):
        plant = Plant()
        hw = Simproxy.lemonator(plant)
        sim = Simulator(plant, Controller(), True)
        wpump = hw.water_pump
        spump = hw.sirup_pump
        afstand = hw.distance

        sample1 = afstand.read_mm()

        wpump.set(1)
        spump.set(1)


        for i in range(200):
            sim._Simulator__plant.update()

        wpump.set(0)
        spump.set(0)


        print(str(sample1) + " > " + str(afstand.read_mm()))

        self.assertTrue(sample1 > afstand.read_mm())

    def testreflex(self):
        plant = Plant()
        hw = Simproxy.lemonator(plant)
        sim = Simulator(plant, Controller(), True)
        reflex = hw.reflex

        sample1 = reflex.get()

        print("\nbefore removing cup: " + str(reflex.get()))

        #remove the cup
        plant._vessels['mix'].toggle()

        for i in range(20):
            sim._Simulator__plant.update()

        print("after removing cup: " + str(reflex.get()))
        self.assertTrue(sample1 != reflex.get())




unittest.main()
