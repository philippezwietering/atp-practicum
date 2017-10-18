import Controller
import unittest
from ../huibonator/Effector import Effector
from ../huibonator/Sensor import Sensor, TemperatureSensor, LevelSensor, ColourSensor
from ../huibonator/Constants import *
from time import sleep
from ../huibonator/Simulator import Plant, Simulator
import ../huibonator/Simproxy

def runtests(cont, plant, amount):
    if amount < 1:
        print("More than 0 iterations for proper testing")

    for i in range(amount):
        cont.update()
        plant.update()


class controllertests(unittest.TestCase):

    def setUp(self):
        self.plant = Plant()
        self.hw = Simproxy.lemonator(self.plant)
        self.controller = Controller(self.plant)
        self.sim = Simulator(self.plant, self.controller, True)

    def testAPress(self):
        print("Testing functionaly of A press\n")
        plkeypad = self.plant._sensors["keypad"]
        pldistance = self.plant._sensors["distance"]

        #Check to see if controller responded to A press by opening the sirup valve and
        #turning on the sirup pump
        plkeypad.pressKey("A")
        self.controller.update()

        self.assertTrue(self.plant.effectors["pumpB"].isOn())
        self.assertFalse(self.plant.effectors["valveB"].isOn())

        #Check to see if controller turned off sirup pump and valve when treshold is reached
        #Then turns on the water valve and pump
        self.plant._vessels['mix'].amount = 500

        self.controller.update()
        self.assertFalse(self.plant.effectors["pumpB"].isOn())
        self.assertTrue(self.plant.effectors["valveB"].isOn())

        self.assertTrue(self.plant.effectors["pumpA"].isOn())
        self.assertFalse(self.plant.effectors["valveA"].isOn())

        #Check to see if controller turned off water pump and valve when treshold is reahced
        self.plant._vessels['mix'].amount = 1650
        self.controller.update()

        self.assertFalse(self.plant.effectors["pumpA"].isOn())
        self.assertTrue(self.plant.effectors["valveA"].isOn())
        