# This file tests the custom made controller and should be able to check both the cpp and python version

import unittest
from unittest import TestCase

import CustomController
from CustomController import LemonatorErrors, LemonatorState

import SimProxy
import Simulator
import Sensor
import Effector
import Constants

def updateSimulator(simulator, n=1):
    i = 0
    while i < n:
        simulator._Simulator__plant.update()
        simulator._Simulator__controller.update()
        simulator._Simulator__monitor.update()
        i += 1

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
        self.ctl = CustomController.Controller(
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
            proxy.temperatureSensor(self.temperature),
            proxy.levelSensor(self.level),
            proxy.presenceSensor(self.presence),
            proxy.colourSensor(self.colour),
            proxy.keyPad(self.keypad),
            proxy.Lcd(self.lcd))
        self.sim._Simulator__controller = self.ctl
        self.ctl.initialize()
    
    def testInitialStates(self):
        self.assertEqual(self.ctl.state, LemonatorState.IDLE)
        self.assertEqual(self.ctl.errorState, LemonatorErrors.NONE)

    def testInitialEffectorStates(self):
        self.assertFalse(self.heater.isOn())
        self.assertFalse(self.pumpA.isOn())
        self.assertFalse(self.pumpB.isOn())
    
    def testIdleSensorVars(self):
        # This only works when the sim has updated just once, because the temp will immediately go down after that
        updateSimulator(self.sim)

        self.assertTrue(self.presence.readValue())
        self.assertEqual(self.level._convertToValue(), 100)
        self.assertEqual(self.colour._convertToValue(), 50)
        self.assertEqual(self.temperature._convertToValue(), 35.9)

    def testInitialVars(self):
        self.assertEqual(self.ctl.aLevel, Constants.storageMax)
        self.assertEqual(self.ctl.bLevel, Constants.storageMax)

        self.assertEqual(self.keypad.pop(), '\x00')
        self.assertEqual(self.ctl.latestKeyPress, "")
        self.assertEqual(self.ctl.targetLevel, -1)
        self.assertEqual(self.ctl.targetRatio, -1)
        self.assertEqual(self.ctl.targetTemperature, -1)
        self.assertEqual(self.ctl.inputLevel, "")
        self.assertEqual(self.ctl.inputRatio, "")
        self.assertEqual(self.ctl.inputTemperature, "")
    
    def testInitialLCD(self):
        lines = self.lcd.getLines()

        self.assertEqual(list(lines), [' ' * 20] * 4)
    
    def testInitialsLeds(self):
        updateSimulator(self.sim)

        self.assertTrue(self.ledRedA.isOn())
        self.assertFalse(self.ledGreenA.isOn())
        self.assertTrue(self.ledRedB.isOn())
        self.assertFalse(self.ledGreenB.isOn())
        self.assertTrue(self.ledGreenM.isOn())
        self.assertFalse(self.ledYellowM.isOn())
    
    def testIdleState(self):
        updateSimulator(self.sim)

        self.testInitialStates() # These should still hold
        self.testInitialsLeds()
        self.assertEqual(list(self.lcd.getLines())[0].strip(), "LEMONATOR")
        self.assertEqual(list(self.lcd.getLines())[1].strip(), "--------------------")
        self.assertEqual(list(self.lcd.getLines())[2].strip(), "Press A to start")
        self.assertEqual(list(self.lcd.getLines())[3].strip(), "Press # to cancel")
    
    def testStartMenu(self):
        updateSimulator(self.sim)

        self.testIdleState()

        self.keypad.push("#")
        updateSimulator(self.sim)

        self.testIdleState()

        self.keypad.push("*")
        updateSimulator(self.sim)

        self.testIdleState()

        self.keypad.push("A")
        updateSimulator(self.sim)

        self.assertEqual(self.ctl.state, LemonatorState.USER_SELECTING_RATIO)

    def testUserSelectingRatioLcd(self):
        self.ctl.state = LemonatorState.USER_SELECTING_RATIO
        updateSimulator(self.sim)

        self.assertEqual(list(self.lcd.getLines())[0].strip(), "LEMONATOR")
        self.assertEqual(list(self.lcd.getLines())[1].strip(), "--------------------")
        self.assertEqual(list(self.lcd.getLines())[2].strip(), "Desired vol. ratio:")
        self.assertEqual(list(self.lcd.getLines())[3].strip(), "1 to  | B to A (*)")
    
    def testUserSelectingRatioInput(self):
        self.testUserSelectingRatioLcd()

        self.keypad.push("5")
        updateSimulator(self.sim)

        self.assertEqual(list(self.lcd.getLines())[3].strip(), "1 to 5 | B to A (*)")

        self.keypad.push("0")
        updateSimulator(self.sim)

        self.assertEqual(list(self.lcd.getLines())[3].strip(), "1 to 50 | B to A (*)")

        self.keypad.push("*")
        updateSimulator(self.sim)

        self.assertEqual(self.ctl.state, LemonatorState.USER_SELECTING_VOLUME)
        self.assertEqual(self.ctl.errorState, LemonatorErrors.NONE)
        self.assertEqual(self.ctl.targetRatio, 50)

        self.keypad.push("#")
        updateSimulator(self.sim)

        self.testIdleState()

        self.testUserSelectingRatioLcd()
        self.keypad.push("A")
        updateSimulator(self.sim)

        self.assertEqual(self.ctl.inputRatio, "")

        self.keypad.push("*")
        updateSimulator(self.sim, 2)

        self.assertEqual(self.ctl.errorState, LemonatorErrors.INVALID_INPUT)
        self.assertEqual(self.ctl.state, LemonatorState.ERROR)

    def testUserSelectingVolumeLcd(self):
        self.ctl.state = LemonatorState.USER_SELECTING_VOLUME
        updateSimulator(self.sim)

        self.assertEqual(list(self.lcd.getLines())[0].strip(), "LEMONATOR")
        self.assertEqual(list(self.lcd.getLines())[1].strip(), "--------------------")
        self.assertEqual(list(self.lcd.getLines())[2].strip(), "Desired volume:")
        self.assertEqual(list(self.lcd.getLines())[3].strip(), "mL (*)")
    
    def testUserSelectingVolumeInput(self):
        self.testUserSelectingVolumeLcd()
        self.ctl.targetRatio = 9

        self.keypad.push("1")
        updateSimulator(self.sim)

        self.assertEqual(list(self.lcd.getLines())[3].strip(), "1 mL (*)")

        self.keypad.push("0")
        updateSimulator(self.sim)

        self.assertEqual(list(self.lcd.getLines())[3].strip(), "10 mL (*)")
        self.assertEqual(self.ctl.inputLevel, "10")

        self.keypad.push("*")
        updateSimulator(self.sim)

        self.assertEqual(self.ctl.state, LemonatorState.USER_SELECTING_HEAT)
        self.assertEqual(self.ctl.errorState, LemonatorErrors.NONE)
        self.assertEqual(self.ctl.targetLevel, 10)

        self.keypad.push("#")
        updateSimulator(self.sim)

        self.testIdleState()

        self.testUserSelectingVolumeLcd()
        self.ctl.targetRatio = 9

        self.keypad.push("0")
        updateSimulator(self.sim)
        self.keypad.push("*")
        updateSimulator(self.sim, 2)

        self.assertEqual(self.ctl.errorState, LemonatorErrors.INVALID_INPUT)

        self.keypad.push("#")
        updateSimulator(self.sim)
        self.testUserSelectingVolumeLcd()
        self.ctl.targetRatio = 1
        self.ctl.bLevel = 2

        self.keypad.push("5")
        updateSimulator(self.sim)
        self.keypad.push("*")
        updateSimulator(self.sim)

        self.assertEqual(self.ctl.errorState, LemonatorErrors.B_SHORTAGE)

        self.keypad.push("#")
        updateSimulator(self.sim)
        self.testUserSelectingVolumeLcd()
        self.ctl.targetRatio = 1
        self.ctl.bLevel = 100000
        self.ctl.aLevel = 3

        self.keypad.push("7")
        updateSimulator(self.sim)
        self.keypad.push("*")
        updateSimulator(self.sim)

        self.assertEqual(self.ctl.errorState, LemonatorErrors.A_SHORTAGE)

        self.keypad.push("#")
        updateSimulator(self.sim)
        self.keypad.push("#")
        updateSimulator(self.sim)
        self.testUserSelectingVolumeLcd()
        self.ctl.targetRatio = 1
        self.ctl.bLevel = 10000
        self.ctl.aLevel = 10000

        self.keypad.push("3")
        updateSimulator(self.sim)
        self.keypad.push("3")
        updateSimulator(self.sim)
        self.keypad.push("3")
        updateSimulator(self.sim)
        self.keypad.push("3")
        updateSimulator(self.sim)
        self.keypad.push("*")
        updateSimulator(self.sim)

        self.assertEqual(self.ctl.errorState, LemonatorErrors.INVALID_INPUT)
    
    def testUserSelectingHeaterLcd(self):
        self.ctl.state = LemonatorState.USER_SELECTING_HEAT
        updateSimulator(self.sim)

        self.assertEqual(list(self.lcd.getLines())[0].strip(), "LEMONATOR")
        self.assertEqual(list(self.lcd.getLines())[1].strip(), "--------------------")
        self.assertEqual(list(self.lcd.getLines())[2].strip(), "Desired temperature:")
        self.assertEqual(list(self.lcd.getLines())[3].strip(), "deg C (*)")
    
    def testUserSelectingHeaterInput(self):
        self.testUserSelectingHeaterLcd()
        self.ctl.targetRatio = 4
        self.ctl.targetLevel = 50

        self.keypad.push("3")
        updateSimulator(self.sim)
        
        self.assertEqual(list(self.lcd.getLines())[3].strip(), "3 deg C (*)")

        self.keypad.push("*")
        updateSimulator(self.sim)

        self.assertEqual(self.ctl.state, LemonatorState.DISPENSING_B)
        self.assertEqual(self.ctl.errorState, LemonatorErrors.NONE)
        self.assertEqual(self.ctl.targetTemperature, Constants.environmentTemp)

        self.keypad.push("#")
        updateSimulator(self.sim)

        self.testUserSelectingHeaterLcd()
        self.ctl.targetRatio = 4
        self.ctl.targetLevel = 50

        self.ctl.inputTemperature = "60"
        updateSimulator(self.sim)

        self.assertEqual(list(self.lcd.getLines())[3].strip(), "60 deg C (*)")
        self.keypad.push("*")
        updateSimulator(self.sim)
        
        self.assertEqual(self.ctl.targetTemperature, 60)

        self.keypad.push("#")
        updateSimulator(self.sim)

        self.testUserSelectingHeaterLcd()
        self.ctl.targetRatio = 4
        self.ctl.targetLevel = 50
        self.ctl.inputTemperature = "95"

        self.keypad.push("*")
        updateSimulator(self.sim)

        self.assertEqual(self.ctl.errorState, LemonatorErrors.TEMP_TOO_HIGH)
        self.assertEqual(self.ctl.targetTemperature, -1)

        self.keypad.push("#")
        updateSimulator(self.sim)

        self.testUserSelectingHeaterLcd()
        self.ctl.targetRatio = 4
        self.ctl.targetLevel = 50

        self.keypad.push("*")
        updateSimulator(self.sim)

        self.assertEqual(self.ctl.errorState, LemonatorErrors.INVALID_INPUT)
    
    def testErrorMessages(self):
        self.testIdleState()

        self.ctl.errorState = LemonatorErrors.NONE
        updateSimulator(self.sim)

        self.assertEqual(list(self.lcd.getLines())[0].strip(), "LEMONATOR")
        self.assertEqual(list(self.lcd.getLines())[1].strip(), "--------------------")
        self.assertEqual(list(self.lcd.getLines())[2].strip(), "Press A to start")
        self.assertEqual(list(self.lcd.getLines())[3].strip(), "Press # to cancel")

        self.ctl.errorState = LemonatorErrors.EMPTY_VESSEL_A
        updateSimulator(self.sim)

        self.assertEqual(list(self.lcd.getLines())[0].strip(), "ERROR")
        self.assertEqual(list(self.lcd.getLines())[1].strip(), "--------------------")
        self.assertEqual(list(self.lcd.getLines())[2].strip(), "Vessel A is empty")
        self.assertEqual(list(self.lcd.getLines())[3].strip(), "Press # to return")

        self.ctl.errorState = LemonatorErrors.EMPTY_VESSEL_B
        updateSimulator(self.sim)

        self.assertEqual(list(self.lcd.getLines())[2].strip(), "Vessel B is empty")

        self.ctl.errorState = LemonatorErrors.INVALID_INPUT
        updateSimulator(self.sim)

        self.assertEqual(list(self.lcd.getLines())[2].strip(), "Input is invalid")

        self.ctl.errorState = LemonatorErrors.TEMP_TOO_HIGH
        updateSimulator(self.sim)

        self.assertEqual(list(self.lcd.getLines())[2].strip(), "Input temp too high")

        self.ctl.errorState = LemonatorErrors.CUP_REMOVED
        updateSimulator(self.sim)

        self.assertEqual(list(self.lcd.getLines())[2].strip(), "Cup was removed")

        self.ctl.errorState = LemonatorErrors.A_SHORTAGE
        updateSimulator(self.sim)

        self.assertEqual(list(self.lcd.getLines())[2].strip(), "Too little in A")

        self.ctl.errorState = LemonatorErrors.B_SHORTAGE
        updateSimulator(self.sim)

        self.assertEqual(list(self.lcd.getLines())[2].strip(), "Too little in B")

    def testDispensingBState(self):
        self.ctl.state = LemonatorState.DISPENSING_B
        self.ctl.aLevel = 2000
        self.ctl.bLevel = 2000
        self.ctl.targetLevel = 100
        self.ctl.targetRatio = 9
        self.ctl.startLevel = 100

        updateSimulator(self.sim, 10) # It takes a few cycles / seconds for liquid to reach the cup

        self.assertEqual(list(self.lcd.getLines())[0].strip(), "LEMONATOR")
        self.assertEqual(list(self.lcd.getLines())[1].strip(), "--------------------")
        self.assertEqual(list(self.lcd.getLines())[2].strip(), "Dispensing B")
        self.assertEqual(list(self.lcd.getLines())[3].strip(), f"{100+Constants.flowRate*5}/110 progress")

        self.assertFalse(self.pumpA.isOn())
        self.assertFalse(self.valveA.isOn())
        self.assertTrue(self.pumpB.isOn())
        self.assertFalse(self.valveB.isOn())

        self.assertTrue(self.ledRedA.isOn())
        self.assertFalse(self.ledGreenA.isOn())
        self.assertFalse(self.ledRedB.isOn())
        self.assertTrue(self.ledGreenB.isOn())

        updateSimulator(self.sim, 5)

        self.assertEqual(self.ctl.state, LemonatorState.DISPENSING_A)
        self.assertEqual(self.level._convertToValue(), 110)
        self.assertEqual(self.ctl.bLevel, 1990)

        self.assertFalse(self.pumpA.isOn())
        self.assertTrue(self.valveA.isOn())
        self.assertFalse(self.pumpB.isOn())
        self.assertTrue(self.valveB.isOn())

    def testDispensingBStateCancel(self):
        self.ctl.state = LemonatorState.DISPENSING_B
        self.ctl.aLevel = 2000
        self.ctl.bLevel = 2000
        self.ctl.targetLevel = 100
        self.ctl.targetRatio = 9
        self.ctl.startLevel = 100

        updateSimulator(self.sim, 10)

        self.keypad.push("#")
        updateSimulator(self.sim)

        self.assertEqual(self.ctl.state, LemonatorState.IDLE)
        self.assertFalse(self.pumpA.isOn())
        self.assertTrue(self.valveA.isOn())
        self.assertFalse(self.pumpB.isOn())
        self.assertTrue(self.valveB.isOn())
    
    def testCupRemovalDispensingB(self):
        self.ctl.state = LemonatorState.DISPENSING_B
        self.ctl.aLevel = 2000
        self.ctl.bLevel = 2000
        self.ctl.targetLevel = 100
        self.ctl.targetRatio = 9
        self.ctl.startLevel = 100

        updateSimulator(self.sim, 10)

        self.vesselMix.setPresence(False)
        updateSimulator(self.sim)

        self.assertEqual(self.ctl.errorState, LemonatorErrors.CUP_REMOVED)
        self.assertFalse(self.pumpA.isOn())
        self.assertTrue(self.valveA.isOn())
        self.assertFalse(self.pumpB.isOn())
        self.assertTrue(self.valveB.isOn())
    
    # def testShortageB(self):
    #     self.ctl.state = LemonatorState.DISPENSING_B
    #     self.ctl.aLevel = 2000
    #     self.ctl.bLevel = 30
    #     self.ctl.targetLevel = 100
    #     self.ctl.targetRatio = 2
    #     self.ctl.startLevel = 100

    #     updateSimulator(self.sim, 50)

    #     self.assertEqual(self.ctl.errorState, LemonatorErrors.B_SHORTAGE)
    
    def testDispensingAState(self):
        self.ctl.state = LemonatorState.DISPENSING_B
        self.ctl.aLevel = 2000
        self.ctl.bLevel = 2000
        self.ctl.targetLevel = 100
        self.ctl.targetRatio = 9
        self.ctl.startLevel = 100

        updateSimulator(self.sim, 15)

        self.assertEqual(self.ctl.state, LemonatorState.DISPENSING_A)
        self.assertEqual(self.ctl.aLevel, 2000)
        self.assertEqual(self.level._convertToValue(), 110)

        updateSimulator(self.sim, 10)

        self.assertEqual(list(self.lcd.getLines())[0].strip(), "LEMONATOR")
        self.assertEqual(list(self.lcd.getLines())[1].strip(), "--------------------")
        self.assertEqual(list(self.lcd.getLines())[2].strip(), "Dispensing A")
        self.assertEqual(list(self.lcd.getLines())[3].strip(), "117/200 progress")

        self.assertTrue(self.pumpA.isOn())
        self.assertFalse(self.valveA.isOn())
        self.assertFalse(self.pumpB.isOn())
        self.assertFalse(self.valveB.isOn())

        self.assertFalse(self.ledRedA.isOn())
        self.assertTrue(self.ledGreenA.isOn())
        self.assertTrue(self.ledRedB.isOn())
        self.assertFalse(self.ledGreenB.isOn())

        updateSimulator(self.sim, 83)

        self.assertEqual(self.ctl.state, LemonatorState.IDLE)
        self.assertEqual(self.level._convertToValue(), 200)

    def testDispensingAStateCancel(self):
        self.ctl.state = LemonatorState.DISPENSING_B
        self.ctl.aLevel = 2000
        self.ctl.bLevel = 2000
        self.ctl.targetLevel = 100
        self.ctl.targetRatio = 9
        self.ctl.startLevel = 100

        updateSimulator(self.sim, 25)

        self.assertEqual(self.ctl.state, LemonatorState.DISPENSING_A)

        self.keypad.push("#")
        updateSimulator(self.sim)

        self.assertEqual(self.ctl.state, LemonatorState.IDLE)
        self.assertFalse(self.pumpA.isOn())
        self.assertTrue(self.valveA.isOn())
        self.assertFalse(self.pumpB.isOn())
        self.assertTrue(self.valveB.isOn())
    
    def testCupRemovalDispensingA(self):
        self.ctl.state = LemonatorState.DISPENSING_B
        self.ctl.aLevel = 2000
        self.ctl.bLevel = 2000
        self.ctl.targetLevel = 100
        self.ctl.targetRatio = 9
        self.ctl.startLevel = 100

        updateSimulator(self.sim, 25)

        self.assertEqual(self.ctl.state, LemonatorState.DISPENSING_A)

        self.vesselMix.setPresence(False)
        updateSimulator(self.sim)

        self.assertEqual(self.ctl.errorState, LemonatorErrors.CUP_REMOVED)
        self.assertFalse(self.pumpA.isOn())
        self.assertTrue(self.valveA.isOn())
        self.assertFalse(self.pumpB.isOn())
        self.assertTrue(self.valveB.isOn())

    def testHeaterFunctionality(self):
        self.ctl.state = LemonatorState.DISPENSING_B
        self.ctl.aLevel = 2000
        self.ctl.bLevel = 2000
        self.ctl.targetLevel = 100
        self.ctl.targetRatio = 9
        self.ctl.startLevel = 100
        self.ctl.targetTemperature = 50

        updateSimulator(self.sim, 7)

        self.assertTrue(self.heater.isOn())

        tempTemp = self.temperature._convertToValue()
        updateSimulator(self.sim)

        self.assertEqual(tempTemp + Constants.heatRate, self.temperature._convertToValue())

        self.ctl.targetTemperature = 30
        updateSimulator(self.sim)

        self.assertFalse(self.heater.isOn())
        self.assertTrue(tempTemp + Constants.heatRate - Constants.temperatureDecay, self.temperature._convertToValue())

        self.ctl.targetTemperature = 70
        self.keypad.push("#")
        updateSimulator(self.sim)

        self.assertFalse(self.heater.isOn())
    
    def testHeaterCupRemoval(self):
        self.ctl.state = LemonatorState.DISPENSING_B
        self.ctl.aLevel = 2000
        self.ctl.bLevel = 2000
        self.ctl.targetLevel = 100
        self.ctl.targetRatio = 9
        self.ctl.startLevel = 100
        self.ctl.targetTemperature = 50

        updateSimulator(self.sim, 7)

        self.vesselMix.setPresence(False)
        updateSimulator(self.sim)

        self.assertFalse(self.heater.isOn())
        self.assertEqual(self.temperature._convertToValue(), Constants.environmentTemp + 1)