# This file unittests the functionality of the plant (so it is just a little bit less boring then the interface testing),
# so without any usage of any kind of controller

import unittest
from unittest import TestCase
from unittest.mock import Mock
from Vessel import *
from Effector import *
from Sensor import *
import Constants

class testNormalVessel(TestCase):
    def setUp(self):
        self.flowToVessel = Vessel(amount = 0, colour = 0, temperature = 0, flowTo = None)
        self.vessel = Vessel(amount = 1000, colour = 10, temperature = 20, flowTo = self.flowToVessel)

    def testVesselConstructor(self):
        # Nothing has updated yet or been done with the vessel, so it should remain the exact same as in the constructor

        self.assertEqual(1000, self.vessel._amount)
        self.assertEqual(10, self.vessel._colour)
        self.assertEqual(20, self.vessel._temperature)
        self.assertIs(self.flowToVessel, self.vessel._flowTo)
        self.assertTrue(self.vessel._presence)

    def testVesselGetters(self):
        # Same test conditions as in the previous test, just retrieving the data in a different way

        self.assertEqual(1000, self.vessel.getFluidAmount())
        self.assertEqual(10, self.vessel.getColour())
        self.assertEqual(20, self.vessel.getTemperature())
        self.assertTrue(self.vessel.getPresence())

    def testNormalFlow(self):
        # In this test the basic flow functionality is tested
        self.vessel.flow()

        self.assertEqual(Constants.flowRate, self.flowToVessel._amount)
        self.assertEqual(self.vessel._amount, 1000 - Constants.flowRate)

    def testFlowWithEmptyStartVessel(self):
        # This test raises an error, because the flowIn method doesn't check the amount of liquid it takes in and always performs a division.
        # This could be fixed by checking if the vessel is empty before executing the flowIn method

        # Due to time constraints I have not fixed this bug myself
        emptyVessel = Vessel(amount = 0, flowTo = self.flowToVessel)
        emptyVessel.flow()

        self.assertEqual(0, emptyVessel._amount)
        self.assertEqual(0, self.flowToVessel._amount)
    
    def testFlowWithVesselEmptierThenFlowRate(self):
        nearEmptyVessel = Vessel(amount = Constants.flowRate / 2, flowTo = self.flowToVessel)
        nearEmptyVessel.flow()

        self.assertEqual(0, nearEmptyVessel._amount)
        self.assertEqual(Constants.flowRate / 2, self.flowToVessel._amount)

    def testFlowWithFlowToFull(self):
        fullVessel = Vessel(amount = Constants.storageMax)
        justAVessel = Vessel(amount = Constants.flowRate * 10, flowTo = fullVessel)

        justAVessel.flow()

        self.assertEqual(fullVessel._amount, Constants.storageMax)
        self.assertEqual(justAVessel._amount, Constants.flowRate * 9)

    def testFlowWithFlowToAlmostFull(self):
        # This test fails, because the internal logic of flowIn is incosistent (a near empty vessel should be filled even if the flowrate is higher than empty part).
        # Due to time constraints I will not fix this
        almostFullVessel = Vessel(amount = Constants.storageMax - 0.5 * Constants.flowRate)
        aVessel = Vessel(amount = Constants.flowRate * 5, flowTo = almostFullVessel)

        aVessel.flow()

        self.assertEqual(almostFullVessel._amount, Constants.storageMax)
        self.assertEqual(aVessel._amount, Constants.flowRate * 4)

    # Since the flow method calls the flowIn method, flowIn should also be already tested, except for the colour part
    def testFlowInColourEmpty(self):
        self.flowToVessel.flowIn(10, 20)

        self.assertEqual(self.flowToVessel._colour, 20)

    def testFlowInColourMixed(self):
        someVessel = Vessel(amount = 100, colour = 10)

        someVessel.flowIn(100, 30)

        self.assertEqual(someVessel._colour, 20)

    # In the other cases of the flowIn funtion, the colour isn't adjusted at all

class testMixtureVessel(TestCase):
    def setUp(self):
        self.mixtureVessel = MixtureVessel(amount = 50, colour = 20, temperature = 30)
    
    def testMixtureVesselConstructor(self):
        self.assertTrue(self.mixtureVessel._presence)
        self.assertEqual(self.mixtureVessel._amount, 50)
        self.assertEqual(self.mixtureVessel._colour, 20)
        self.assertEqual(self.mixtureVessel._temperature, 30)
        self.assertIsNone(self.mixtureVessel._flowTo)
        self.assertFalse(self.mixtureVessel._heat)
    
    def testMixtureVesselGets(self):
        self.assertTrue(self.mixtureVessel.getPresence())
        self.assertEqual(self.mixtureVessel.getColour(), 20)
        self.assertEqual(self.mixtureVessel.getFluidAmount(), 50)
        self.assertEqual(self.mixtureVessel.getTemperature(), 30)

    def testMixtureVesselHeat(self):
        self.mixtureVessel.heat(True)

        self.assertTrue(self.mixtureVessel._heat)

        self.mixtureVessel.heat()

        self.assertFalse(self.mixtureVessel._heat)

    # Testing all vessel variables related to the presence, which can only be set for mixturevessels
    def testMixtureVesselPresence(self):
        self.mixtureVessel.setPresence(True)

        self.assertEqual(self.mixtureVessel._amount, 50)
        self.assertEqual(self.mixtureVessel._colour, 20)
        self.assertEqual(self.mixtureVessel._temperature, 30)
        self.assertTrue(self.mixtureVessel._presence)

        self.mixtureVessel.setPresence()

        self.assertEqual(self.mixtureVessel._amount, 0)
        self.assertEqual(self.mixtureVessel._colour, 0)
        self.assertEqual(self.mixtureVessel._temperature, Constants.environmentTemp)
        self.assertFalse(self.mixtureVessel._presence)

        # Nothing should happen, because the mixtureVessel is not present
        self.mixtureVessel.flowIn(100, 20)

        self.assertEqual(self.mixtureVessel._amount, 0)
        self.assertEqual(self.mixtureVessel._colour, 0)
        self.assertEqual(self.mixtureVessel._temperature, Constants.environmentTemp)
        self.assertFalse(self.mixtureVessel._presence)

    def testMixtureVesselUpdate(self):
        # Just to make sure everything is in working order

        self.assertEqual(self.mixtureVessel._amount, 50)
        self.assertEqual(self.mixtureVessel._colour, 20)
        self.assertEqual(self.mixtureVessel._temperature, 30)
        self.assertTrue(self.mixtureVessel._presence)
        self.assertFalse(self.mixtureVessel._heat)

        self.mixtureVessel.update()

        # Also checking the other variables to make sure there are no side effects
        self.assertEqual(self.mixtureVessel._amount, 50)
        self.assertEqual(self.mixtureVessel._colour, 20)
        self.assertEqual(self.mixtureVessel._temperature, 30 - Constants.temperatureDecay)
        self.assertTrue(self.mixtureVessel._presence)
        self.assertFalse(self.mixtureVessel._heat)

        self.mixtureVessel.heat(True)
        self.mixtureVessel.update()

        self.assertEqual(self.mixtureVessel._amount, 50)
        self.assertEqual(self.mixtureVessel._colour, 20)
        self.assertEqual(self.mixtureVessel._temperature, 30 - Constants.temperatureDecay + Constants.heatRate)
        self.assertTrue(self.mixtureVessel._presence)
        self.assertTrue(self.mixtureVessel._heat)

class testEffectorBase(TestCase):
    def setUp(self):
        self.vessel = Vessel()
        self.effector = Effector(self.vessel)
    
    def testEffectorConstructor(self):
        self.assertFalse(self.effector._value)
        self.assertIs(self.vessel, self.effector._vessel)
    
    def testEffectorSwitches(self):
        self.assertFalse(self.effector._value)
        self.assertFalse(self.effector.isOn())

        self.effector.switchOff()

        self.assertFalse(self.effector._value)
        self.assertFalse(self.effector.isOn())

        self.effector.switchOn()

        self.assertTrue(self.effector._value)
        self.assertTrue(self.effector.isOn())

        self.effector.switchOn()

        self.assertTrue(self.effector._value)
        self.assertTrue(self.effector.isOn())

class testPump(TestCase):
    def setUp(self):
        # We have already fully test Vessel, so we only want to know if its functions get called succesfully

        self.vessel = Mock(spec_set=['flow'])
        self.pump = Pump(self.vessel)

    # Technically not all variables should probably be checked, since they have already been tested in Effector, 
    # but it doesn't hurt the test quality either
    def testPumpConstructor(self):
        self.assertIs(self.pump._vessel, self.vessel)
        self.assertFalse(self.pump._value)
        self.assertEqual(self.pump._pressure, 0)
    
    def testPumpUpdateNothing(self):
        self.assertEqual(self.pump._pressure, 0)
        self.assertFalse(self.pump._value)

        self.pump.update()
        
        self.assertEqual(self.pump._pressure, 0)
    
    def testPumpUpdateRampUp(self):
        self.assertEqual(self.pump._pressure, 0)
        self.assertFalse(self.pump._value)

        self.pump.switchOn()

        self.assertEqual(self.pump._pressure, 0)
        self.assertTrue(self.pump._value)

        self.pump.update()

        self.assertEqual(self.pump._pressure, 100 / Constants.pressureRampUp)

    def testPumpUpdateRampDown(self):
        # Just setting the pressure ourselves so we can check if it will decrease naturally after that

        self.pump._pressure = 50
        self.assertFalse(self.pump._value)

        self.pump.update()

        self.assertEqual(self.pump._pressure, 50 - 100 / Constants.pressureRampDown)


    def testPumpFlow(self):
        self.pump._pressure = 100
        self.pump.switchOn()

        self.pump.update()

        self.assertEqual(self.pump._pressure, 200)
        # It takes one tick to start to the flow
        self.vessel.flow.assert_not_called()

        self.pump.update()

        self.assertEqual(self.pump._pressure, 200)
        self.vessel.flow.assert_called_once_with()

    def testPumpVesselIsNone(self):
        # Check the behaviour is no vessel is present
        self.pump._vessel = None

        self.assertEqual(self.pump._pressure, 0)
        self.assertFalse(self.pump._value)

        self.pump.switchOn()

        self.pump.update()

        self.assertEqual(self.pump._pressure, 100/Constants.pressureRampUp)
        # I have searched extensively, but I couldn't find a mock object type that masks as None, 
        # so we can't explicitly test if the flow method is called on the None object or not. 
        # So we will have to be satisfied with the absence of an Error raised because of a method call on None

# From now on only testing the non-parent functions
class testValve(TestCase):
    def setUp(self):
        self.pump = Mock(spec=Pump)
        self.vessel = Mock(spec_set=[''])
        self.valve = Valve(self.vessel)

    def testValveConstructor(self):
        self.assertFalse(self.valve._value)
        self.assertIs(self.vessel, self.valve._vessel)
    
    def testValveSetPump(self):
        # Before calling the attribute doesn't even exist yet, so we can't test for its existence

        self.valve.setPump(self.pump)
        self.assertIs(self.valve._Valve__pump, self.pump)
    
    def testValveUpdate(self):
        self.valve.setPump(self.pump)
        self.pump._pressure = 100

        self.valve.update()

        self.assertEqual(self.pump._pressure, 100)

        self.valve.switchOn()
        self.assertEqual(self.pump._pressure, 100)

        self.valve.update()

        self.assertEqual(self.pump._pressure, 0)

class testHeater(TestCase):
    def setUp(self):
        self.vessel = MixtureVessel()
        self.heater = Heater(self.vessel)

    def testHeaterConstructor(self):
        self.assertFalse(self.heater._value)
        self.assertIs(self.heater._vessel, self.vessel)
    
    def testHeaterUpdate(self):
        # Wasn't able to test this properly with mocks the way I wanted it, because of the way heat is implemented

        temp = self.vessel._temperature
        self.heater.update()

        # Because it is still switched off
        self.assertEqual(self.vessel._temperature, temp)

        self.heater.switchOn()

        self.heater.update()
        self.vessel.update()

        self.assertEqual(self.vessel._temperature, temp + Constants.heatRate)

class testLed(TestCase):
    def setUp(self):
        self.ledColour = Mock()
        self.led = Led(self.ledColour)
    
    def testLedInitialization(self):
        self.assertIs(self.ledColour, self.led._Led__colour)
        self.assertFalse(self.led._value)
        self.assertIsNone(self.led._vessel)
    
    def testLedGetColour(self):
        self.assertIs(self.ledColour, self.led.getColour())
    
    def testLedToggle(self):
        self.assertFalse(self.led._value)
        
        self.led.toggle()

        self.assertTrue(self.led._value)

        self.led.toggle()

        self.assertFalse(self.led._value)

class testLcd(TestCase):
    def setUp(self):
        self.lcd = LCD()
    
    def testLcdInitialization(self):
        self.assertIsNone(self.lcd._vessel)
        self.assertFalse(self.lcd._value)
        self.assertEqual(self.lcd._LCD__lines, [[], [], [], []])
        self.assertEqual(self.lcd._LCD__cursor, (0, 0))
    
    def testPushString(self):
        self.assertEqual(self.lcd._LCD__lines, [[], [], [], []])
        # So the lcd is properly empty initialized
        self.lcd.clear()

        self.lcd.pushString("Niet 20 tekens")

        self.assertEqual(''.join(self.lcd._LCD__lines[0]), "Niet 20 tekens      ")

        self.lcd.pushString("\x0cNieuwe tekens") # For testing the \x0c command
        
        self.assertEqual(''.join(self.lcd._LCD__lines[0]), "Nieuwe tekens       ")

        self.lcd.pushString(" erbij")

        self.assertEqual(''.join(self.lcd._LCD__lines[0]), "Nieuwe tekens erbij ")

        self.lcd.pushString("\x0cIets dat langer is dan 20 tekens")

        self.assertEqual(''.join(self.lcd._LCD__lines[0]), "an 20 tekensger is d") # For some reason this implementation doesn't think at all

        self.lcd.pushString("\x0cIets dat langer is \ndan 20 tekens")
        
        self.assertEqual(''.join(self.lcd._LCD__lines[0]), "Iets dat langer is  ")
        self.assertEqual(''.join(self.lcd._LCD__lines[1]), "dan 20 tekens       ")

        # TODO
        # self.lcd.pushString("\x0cHier\teen tab")
        # self.assertEqual(''.join(self.lcd._LCD__lines[0]), "Hier      een tab")

    def testLcdGetLines(self):
        for line in self.lcd._LCD__lines:
            self.assertEqual([], line) # String should be empty, we didn't put anything on screen

        self.lcd._LCD__lines = [["Dit"], ["is"], ["een"], ["test"]]

        self.assertIsInstance(self.lcd.getLines(), map) # This is a really bad way to implement the getLines function and not a lot I can test on it,
                                                        # because map is really really annoying to deal with
    
    def testLcdClear(self):
        self.assertEqual(self.lcd._LCD__lines, [[], [], [], []])

        self.lcd._LCD__lines = [["Dit"], ["is"], ["een"], ["test"]]
        self.lcd.clear()

        # This is just fugly
        self.assertEqual(self.lcd._LCD__lines, [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']])
    
    # Work in progress
    def testLcdPut(self):
        pass

class testSensorBase(TestCase):
    def setUp(self):
        self.vessel = Vessel()
        self.sensor = Sensor(self.vessel)
    
    def testSensorConstructor(self):
        self.assertIs(self.sensor._vessel, self.vessel)
        self.assertEqual(self.sensor._value, 0)
        self.assertEqual(self.sensor._unitOfMeasure, '')
    
    def testSensorReadValue(self):
        # Testing for the 0 case, sometimes gives troubles
        self.assertEqual(self.sensor._value, self.sensor.readValue())

        self.sensor._value = 3.14159265
        self.assertEqual(3.14, self.sensor.readValue())

        self.sensor._value = -2.91
        self.assertEqual(self.sensor._value, self.sensor.readValue())
    
    def testSensorMeasure(self):
        self.assertEqual("0", self.sensor.measure())

        someUnit = "MegaUnit"
        self.sensor._unitOfMeasure = someUnit
        self.sensor._value = 3.14

        self.assertEqual(str(3.14) + someUnit, self.sensor.measure())
    
    def testSensor_convertToValue(self):
        # Testing for the 0 case, sometimes gives troubles
        self.assertEqual(self.sensor._value, self.sensor.readValue())

        self.sensor._value = 3.14159265
        self.assertEqual(3.14, self.sensor.readValue())

        self.sensor._value = -2.91
        self.assertEqual(self.sensor._value, self.sensor.readValue())

# Again, same as with effectors, only testing 'new' methods, casuse 
class testColourSensor(TestCase):
    def setUp(self):
        self.vessel = Vessel()
        self.csensor = ColourSensor(self.vessel)
    
    def testColourSensorConstructor(self):
        self.assertEqual('%', self.csensor._unitOfMeasure)
        self.assertIs(self.vessel, self.csensor._vessel)

    def testColourSensorUpdate(self):
        self.assertEqual(self.csensor._value, 0)

        self.csensor.update()

        self.assertEqual(self.csensor._value, 0)

        self.vessel._colour = 50
        self.csensor.update()

        self.assertEqual(50 * Constants.colourConversion, self.csensor._value)

    # def testColourSensorUpdateNoVessel(self):
    #     self.assertEqual(self.csensor._value, 0)

    #     self.vessel._colour = 50
    #     self.csensor._vessel = None

    #     self.csensor.update()

    #     self.assertEqual(self.csensor._value, 0)

    def testColourSensor_convertToValue(self):
        self.assertEqual(self.csensor._convertToValue(), 0)

        self.csensor._value = 50

        self.assertEqual(self.csensor._convertToValue(), round(50 / Constants.colourConversion, 2))

class testTemperatureSensor(TestCase):
    def setUp(self):
        self.vessel = Vessel()
        self.tsensor = TemperatureSensor(self.vessel)
    
    def testTemperatureSensorConstructor(self):
        self.assertIs(self.vessel, self.tsensor._vessel)
        self.assertEqual(self.tsensor._unitOfMeasure, '°C')
    
    def testTemperatureSensorUpdate(self):
        self.assertEqual(0, self.tsensor._value)

        self.tsensor.update()

        self.assertEqual(20 * Constants.tempConversion, self.tsensor._value)
    
    def testTemperatureSensor_convertToValue(self):
        self.tsensor.update()
        self.assertEqual(20, self.tsensor._convertToValue())
    
class testLevelSensor(TestCase):
    def setUp(self):
        self.vessel = Vessel()
        self.lsensor = LevelSensor(self.vessel)
    
    def testLevelSensorConstructor(self):
        self.assertIs(self.vessel, self.lsensor._vessel)
        self.assertEqual(self.lsensor._unitOfMeasure, 'ml')
    
    def testLevelSensorUpdate(self):
        self.assertEqual(self.lsensor._value, 0)
        
        self.vessel._amount = 1000
        self.lsensor.update()

        self.assertEqual(self.lsensor._value, 1000 * Constants.levelConversion / pi / 100)

    def testLevelSensor_convertToValue(self):
        self.vessel._amount = 1000
        self.lsensor.update()

        self.assertEqual(self.lsensor._convertToValue(), 1000)

class testPresenceSensor(TestCase):
    def setUp(self):
        self.vessel = MixtureVessel()
        self.psensor = PresenceSensor(self.vessel)

    def testPresenceSensorUpdate(self):
        self.assertEqual(self.psensor._value, 0)

        self.vessel.setPresence()
        self.psensor.update()

        self.assertFalse(self.psensor._value)

        self.vessel.setPresence()
        self.psensor.update()

        self.assertTrue(self.psensor._value)

    def testPresenceSensorReadValue(self):
        self.assertFalse(self.psensor.readValue())

        self.psensor.update()

        self.assertTrue(self.psensor.readValue())

    def testPresenceSensor_convertToValue(self):
        self.assertFalse(self.psensor._convertToValue())

        self.psensor.update()

        self.assertTrue(self.psensor._convertToValue())

class testKeypadSensor(TestCase):
    def setUp(self):
        self.keypad = KeyPad()
    
    def testKeypadSensorConstructor(self):
        self.assertEqual(self.keypad._keysPressed, [])
    
    def testKeypadSensorPush(self):
        teststring = "t"
        self.keypad.push(teststring)

        self.assertEqual(self.keypad._keysPressed, [teststring])

        tweedeteststring = "\n"
        self.keypad.push(tweedeteststring)

        self.assertEqual(self.keypad._keysPressed, [teststring, tweedeteststring])

    def testKeypadSensorPop(self):
        self.keypad.push('a')
        self.keypad.push('b')

        self.assertEqual(self.keypad._keysPressed, ['a','b'])

        a = self.keypad.pop()
        b = self.keypad.pop()
        c = self.keypad.pop()

        self.assertEqual(a, 'a')
        self.assertEqual(b, 'b')
        self.assertEqual(c, '\x00')

if __name__ == "__main__":
    unittest.main()