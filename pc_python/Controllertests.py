import Controller
import imp
import unittest
from ../huibonator/Effector import Effector
from ../huibonator/Sensor import Sensor, TemperatureSensor, LevelSensor, ColourSensor
from ../huibonator/Constants import *
from ../huibonator/Simulator import Plant, Simulator
import ../huibonator/Simproxy

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

        self.assertTrue(self.plant._effectors["pumpB"].isOn())
        self.assertFalse(self.plant._effectors["valveB"].isOn())

        #Check to see if controller turned off sirup pump and valve when treshold is reached
        #Then turns on the water valve and pump
        self.plant._vessels['mix'].amount = 500

        self.controller.update()
        self.assertFalse(self.plant._effectors["pumpB"].isOn())
        self.assertTrue(self.plant._effectors["valveB"].isOn())

        self.assertTrue(self.plant._effectors["pumpA"].isOn())
        self.assertFalse(self.plant._effectors["valveA"].isOn())

        #Check to see if controller turned off water pump and valve when treshold is reahced
        self.plant._vessels['mix'].amount = 1650
        self.controller.update()

        self.assertFalse(self.plant._effectors["pumpA"].isOn())
        self.assertTrue(self.plant._effectors["valveA"].isOn())

    def testRemoval(self):
        print("Testing what happens when cup is removed\n")
        plkeypad = self.plant._sensors["keypad"]
        plreflex = self.plant._sensors["reflex"]

        plkeypad.pressKey("A")
        self.controller.update()
        self.plant._vessels['mix'].amount = 200
        self.plant._vessels['mix'].toggle()
        self.controller.update()

        #Cup is removed so sirup pump and valve should be turned off
        #and state should be "Waiting"
        self.assertFalse(self.plant._effectors["pumpB"].isOn())
        self.assertTrue(self.plant._effectors["valveB"].isOn())
        self.assertTrue(self.controller.state == "Waiting")

        #Same test but now for water pump and valve
        plkeypad.pressKey("A")
        self.controller.update()
        self.plant._vessels['mix'].amount = 1000
        self.plant._vessels['mix'].toggle()
        self.controller.update()

        #Cup is removed so water pump and valve should be turned off
        #and state should be "Waiting"
        self.assertFalse(self.plant._effectors["pumpA"].isOn())
        self.assertTrue(self.plant._effectors["valveA"].isOn())
        self.assertTrue(self.controller.state == "Waiting")

unittest.main()