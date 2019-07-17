# This file unittests the functionality of the plant (so it is just a little bit less boring then the interface testing),
# so without any usage of any kind of controller

import unittest
from unittest import TestCase
from unittest.mock import Mock
from Vessel import *
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
        self.assertEqual(True, self.vessel._presence)

    def testVesselGetters(self):
        # Same test conditions as in the previous test, just retrieving the data in a different way

        self.assertEqual(1000, self.vessel.getFluidAmount())
        self.assertEqual(10, self.vessel.getColour())
        self.assertEqual(20, self.vessel.getTemperature())
        self.assertEqual(True, self.vessel.getPresence())

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
        self.assertEqual(self.mixtureVessel._presence, True)
        self.assertEqual(self.mixtureVessel._amount, 50)
        self.assertEqual(self.mixtureVessel._colour, 20)
        self.assertEqual(self.mixtureVessel._temperature, 30)
        self.assertIs(self.mixtureVessel._flowTo, None)
        self.assertEqual(self.mixtureVessel._heat, False)
    
    def testMixtureVesselGets(self):
        self.assertEqual(self.mixtureVessel.getPresence(), True)
        self.assertEqual(self.mixtureVessel.getColour(), 20)
        self.assertEqual(self.mixtureVessel.getFluidAmount(), 50)
        self.assertEqual(self.mixtureVessel.getTemperature(), 30)

    def testMixtureVesselHeat(self):
        self.mixtureVessel.heat(True)

        self.assertEqual(self.mixtureVessel._heat, True)

        self.mixtureVessel.heat()

        self.assertEqual(self.mixtureVessel._heat, False)

    # Testing all vessel variables related to the presence, which can only be set for mixturevessels
    def testMixtureVesselPresence(self):
        self.mixtureVessel.setPresence(True)

        self.assertEqual(self.mixtureVessel._amount, 50)
        self.assertEqual(self.mixtureVessel._colour, 20)
        self.assertEqual(self.mixtureVessel._temperature, 30)
        self.assertEqual(self.mixtureVessel._presence, True)

        self.mixtureVessel.setPresence()

        self.assertEqual(self.mixtureVessel._amount, 0)
        self.assertEqual(self.mixtureVessel._colour, 0)
        self.assertEqual(self.mixtureVessel._temperature, Constants.environmentTemp)
        self.assertEqual(self.mixtureVessel._presence, False)

        # Nothing should happen, because the mixtureVessel is not present
        self.mixtureVessel.flowIn(100, 20)

        self.assertEqual(self.mixtureVessel._amount, 0)
        self.assertEqual(self.mixtureVessel._colour, 0)
        self.assertEqual(self.mixtureVessel._temperature, Constants.environmentTemp)
        self.assertEqual(self.mixtureVessel._presence, False)

    def testMixtureVesselUpdate(self):
        # Just to make sure everything is in working order

        self.assertEqual(self.mixtureVessel._amount, 50)
        self.assertEqual(self.mixtureVessel._colour, 20)
        self.assertEqual(self.mixtureVessel._temperature, 30)
        self.assertEqual(self.mixtureVessel._presence, True)
        self.assertEqual(self.mixtureVessel._heat, False)

        self.mixtureVessel.update()

        # Also checking the other variables to make sure there are no side effects
        self.assertEqual(self.mixtureVessel._amount, 50)
        self.assertEqual(self.mixtureVessel._colour, 20)
        self.assertEqual(self.mixtureVessel._temperature, 30 - Constants.temperatureDecay)
        self.assertEqual(self.mixtureVessel._presence, True)
        self.assertEqual(self.mixtureVessel._heat, False)

        self.mixtureVessel.heat(True)
        self.mixtureVessel.update()

        self.assertEqual(self.mixtureVessel._amount, 50)
        self.assertEqual(self.mixtureVessel._colour, 20)
        self.assertEqual(self.mixtureVessel._temperature, 30 - Constants.temperatureDecay + Constants.heatRate)
        self.assertEqual(self.mixtureVessel._presence, True)
        self.assertEqual(self.mixtureVessel._heat, True)

if __name__ == "__main__":
    unittest.main()