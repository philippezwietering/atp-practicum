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

def runsim(sim, amount):
    for _ in range(amount):
        sim._Simulator__plant.update()

class Controller:
    def update(self):
        pass

class lemonatorsymtests(unittest.TestCase):
    #in this class the lemonator simulator is tested
    #when possible sensors and actuators will be aproached via the
    #lemonator proxy adapter to prove that this adapter functions as intended

    def setUp(self):
        #default components required for every test
        self.plant = Plant()
        self.hw = Simproxy.lemonator(self.plant)
        self.sim = Simulator(self.plant, Controller(), True)

    def testPump(self):
        print("\ntesting pump functionality")
        pumpA = self.hw.water_pump
        pumpB = self.hw.sirup_pump

        #Directly inside the simulator for checking state
        wpump = self.plant._effectors["pumpA"]
        sipump = self.plant._effectors["pumpB"]

        # when the simulator is created the pump should be off
        # after that we turn the pump on and off
        # and check if it actually does this\n")

        #pump should be off
        self.assertFalse(wpump.isOn())
        self.assertFalse(sipump.isOn())


        #punp should be on
        pumpA.set(1)
        pumpB.set(1)
        self.assertTrue(wpump.isOn())
        self.assertTrue(sipump.isOn())

        #pump should be off again
        pumpA.set(0)
        pumpB.set(0)
        self.assertFalse(wpump.isOn())
        self.assertFalse(sipump.isOn())



    def testMixVesselPresence(self):
        mixves = self.plant._vessels['mix']

        print("\ntest removing and returning of the cup")

        #cup should start out present
        self.assertTrue(mixves.getPresence())

        #cup should be removed
        mixves.toggle()
        runsim(self.sim, 10)
        self.assertFalse(mixves.getPresence())

        #cup should be gone again
        mixves.toggle()
        runsim(self.sim, 10)
        self.assertTrue(mixves.getPresence())

    def testFluidHandling(self):
        wpump = self.hw.water_pump
        spump = self.hw.sirup_pump

        #external approach of vessels to check state changes
        mixves = self.plant._vessels['mix']
        waterves = self.plant._vessels['a']
        sirupves = self.plant._vessels['b']
        print("\ntesting the fluid dynamics of the mixvessel and the storage vessels")

        #initial ammount should be 0
        self.assertTrue(mixves.getFluidAmount() == 0)

        #both suply vessels should be filled up
        self.assertTrue(waterves.getFluidAmount() == storageMax)
        self.assertTrue(sirupves.getFluidAmount() == storageMax)

        #Pumping fluid from the watervessel to the mixves
        wpump.set(1)
        runsim(self.sim, 10)
        wpump.set(0)

        #watervessel should have less fluid
        self.assertTrue(waterves.getFluidAmount() < storageMax)

        #mixves should have more liqid now
        #liquid amount is kept for future measurement
        liqudmeasure = mixves.getFluidAmount()
        self.assertTrue(liqudmeasure > 0)

        #Pumping from the syrupvessel to the mixves
        spump.set(1)
        runsim(self.sim, 10)
        spump.set(0)

        #syrupvessel should have less liquid
        self.assertTrue(sirupves.getFluidAmount() < storageMax)

        #mixves fluid should have increased again
        self.assertTrue(mixves.getFluidAmount() > liqudmeasure)

        #mixves should be empty
        mixves.empty()
        self.assertTrue(mixves.getFluidAmount() == 0)

    def testPrintstate(self):
        print("\ncheck if changes have not broken the printstate\n")
        self.plant.printState()

    def testValve(self):
        print("\ntesting functionality of the valves")
        wpump = self.hw.water_pump
        sipump = self.hw.sirup_pump
        wvalve = self.hw.water_valve
        sivalve = self.hw.sirup_valve

        #direct approach of objects to check state
        extwvalve = self.plant._effectors['valveA']
        extsivalve = self.plant._effectors['valveB']
        waterves = self.plant._vessels['a']
        sirupves = self.plant._vessels['b']

        #valve should start as off
        #pump was tested in pump tested
        self.assertFalse(extwvalve.isOn())
        self.assertFalse(extsivalve.isOn())

        #valves should be on
        wpump.set(1)
        sipump.set(1)
        wvalve.set(1)
        sivalve.set(1)

        self.assertTrue(extwvalve.isOn())
        self.assertTrue(extsivalve.isOn())

        runsim(self.sim, 10)

        #turn off the pump and valve and allow for another
        #update so the air can "flow" out of the valve
        wpump.set(0)
        sipump.set(0)
        runsim(self.sim, 1)
        wvalve.set(0)
        sivalve.set(0)

        #pressure shoud be zero in vessels
        self.assertTrue(waterves._pressure == 0)
        self.assertTrue(sirupves._pressure == 0)



    def testDistance(self):
        print("\ntesting distance sensor")
        wpump = self.hw.water_pump
        spump = self.hw.sirup_pump
        afstand = self.hw.distance

        #measuring distance before adding fluid
        sample1 = afstand.read_mm()

        #Pumping fluid into the mixture vessel
        wpump.set(1)
        spump.set(1)
        runsim(self.sim, 10)
        wpump.set(0)
        spump.set(0)

        #sample1 should be bigger then second measurement because
        #more fluid means the distance from the sensor to the fluid is less
        self.assertTrue(sample1 > afstand.read_mm())

    def testReflex(self):
        print("\ntesting reflex sensor")

        #Cup should start out present
        reflex = self.hw.reflex
        sample1 = reflex.get()

        #remove the cup
        self.plant._vessels['mix'].toggle()

        runsim(self.sim, 10)

        #cup should not be seen anymore
        self.assertTrue(sample1 != reflex.get())

    def testled(self):
        led = self.hw.led_green
        ledy = self.hw.led_yellow

        #external approach to check state of led
        exled = self.plant._effectors['led_green']
        exledy = self.plant._effectors['led_yellow']

        #led should start off
        self.assertFalse(exled.isOn())
        self.assertFalse(exledy.isOn())

        #led should be on
        led.set(1)
        ledy.set(1)
        self.assertTrue(exled.isOn())
        self.assertTrue(exledy.isOn())

        #led should be off again
        led.set(0)
        ledy.set(0)
        self.assertFalse(exled.isOn())
        self.assertFalse(exledy.isOn())

        #testing toggle function for Gui
        exled.toggle()
        self.assertTrue(exled.isOn())
        exled.toggle()
        self.assertFalse(exled.isOn())

    def testKeyPad(self):
        print("\nTesting keypad")
        keypad = self.hw.keypad

        #external aproach to simulate button presses
        exkeypad = self.plant._sensors['keypad']

        #keypad should start with no pressed value
        self.assertTrue(keypad.getc() == '')

        #after pressing a key getc should return that character
        exkeypad.pressKey('A')
        self.assertTrue(keypad.getc() == 'A')

        #after that the value should be empty again
        self.assertTrue(keypad.getc() == '')

        #when a wrong value is given keypad value should remain empty
        exkeypad.pressKey('U')
        self.assertTrue(keypad.getc() == '')

    def testheater(self):
        print("\nTesting heater")
        heater = self.hw.heater

        #external vessel to check temperature changes
        exmixves = self.plant._vessels['mix']
        exheater = self.plant._effectors['heater']

        #heater should start in off state
        self.assertFalse(exheater.isOn())

        #heat value should start at 20
        self.assertTrue(exmixves._temperature == 20)

        #heater should be on
        heater.set(1)
        self.assertTrue(exheater.isOn())
        runsim(self.sim, 10)

        #heater should be off
        heater.set(0)
        self.assertFalse(exheater.isOn())

        #temperature should have risen
        rissentemp = exmixves._temperature
        self.assertTrue(rissentemp > 20)

        #temperature should decay with the heater off
        runsim(self.sim, 100)
        self.assertTrue(exmixves._temperature < rissentemp)

#unittest.main()
