# This file tests the custom made controller and should be able to check both the cpp and python version

import unittest
from unittest import TestCase
import cppimport.import_hook

import CPPController
from CPPController import LemonatorErrors, LemonatorState

import SimProxy
import Simulator
import Sensor
import Effector
import Constants

def updateSimulator(simulator):
    simulator._Simulator__plant.update()
    simulator._Simulator__controller.update()
    simulator._Simulator__monitor.update()

class testControllerStates(TestCase):
    def setUp(self):
        self.sim = Simulator.Simulator(False)

        # These variables are there for convenience
        self.vesselMix = self.sim._Simulator__plant._vessels['mix']
        self.vesselA = self.sim._Simulator__plant._vessels['a']
        self.vesselB = self.sim._Simulator__plant._vessels['b']

        # Create effector objects
        self.pumpA = self.sim._Simulator__plant._effectors['pumpA']
        self.pumpB = self.sim._Simulator__plant._effectors['pumpB']
        self.valveA = self.sim._Simulator__plant._effectors['valveA']
        self.valveB = self.sim._Simulator__plant._effectors['valveB']
        self.heater = self.sim._Simulator__plant._effectors['heater']

        # Create LED's objects
        self.ledRedA = self.sim._Simulator__plant._effectors['redA']
        self.ledGreenA = self.sim._Simulator__plant._effectors['greenA']
        self.ledRedB = self.sim._Simulator__plant._effectors['redB']
        self.ledGreenB = self.sim._Simulator__plant._effectors['greenB']
        self.ledGreenM = self.sim._Simulator__plant._effectors['greenM']
        self.ledYellowM = self.sim._Simulator__plant._effectors['yellowM']

        # Create sensors objects
        self.colour = self.sim._Simulator__plant._sensors['colour']
        self.temperature = self.sim._Simulator__plant._sensors['temp']
        self.level = self.sim._Simulator__plant._sensors['level']
        self.presence = self.sim._Simulator__plant._sensors['presence']

        # Create UI objects
        self.lcd = self.sim._Simulator__plant._effectors['lcd']
        self.keypad = self.sim._Simulator__plant._sensors['keypad']

        proxy = SimProxy.SimProxy
        self.ctl = CPPController.Controller(
            proxy.Effector(self.pumpA),
            proxy.Effector(self.pumpB),
            proxy.Effector(self.valveA),
            proxy.Effector(self.valveB),
            proxy.Led(self.ledRedA),
            proxy.Led(self.ledGreenA),
            proxy.Led(self.ledRedB),
            proxy.Led(self.ledGreenB),
            proxy.Led(self.ledGreenM),
            proxy.Led(self.ledYellowM),
            proxy.Effector(self.heater),
            proxy.colourSensor(self.colour),
            proxy.temperatureSensor(self.temperature),
            proxy.levelSensor(self.level),
            proxy.presenceSensor(self.presence),
            proxy.keyPad(self.keypad),
            proxy.Lcd(self.lcd))
        self.sim._Simulator__controller = self.ctl
        self.ctl.initialize()
    
    def testInitialStates(self):
        self.assertEqual(self.ctl.state, LemonatorState.IDLE)
        self.assertEqual(self.ctl.error, LemonatorErrors.NONE)

        self.assertFalse(self.ctl.heater.isOn())
        self.assertFalse(self.ctl.pumpA.isOn())
        self.assertFalse(self.ctl.pumpB.isOn())

    def testInitialVars(self):
        self.assertEqual(self.ctl.aLevel, Constants.storageMax)
        self.assertEqual(self.ctl.bLevel, Constants.storageMax)

        self.assertEqual(self.ctl.keypad.pop(), '\x00')
        self.assertIsNone(self.ctl.latestKeyPress)
        self.assertIsNone(self.ctl.targetLevel)
        self.assertIsNone(self.ctl.targetRatio)
        self.assertIsNone(self.ctl.targetTemperature)
        self.assertEqual(self.ctl.inputLevel, "")
        self.assertEqual(self.ctl.inputRatio, "")
        self.assertEqual(self.ctl.inputTemperature, "")