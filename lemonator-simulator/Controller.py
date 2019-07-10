from Effector import Effector
from Sensor import Sensor, TemperatureSensor, LevelSensor, ColourSensor
from Constants import *
from time import sleep
from Simulator import Plant, Simulator
import Simproxy

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

    def __init__(self, plant):
        self._plant = plant

    def update(self) -> None:
        # if not self._Controller__effectors['heater'].isOn():
        #     if self._Controller__sensors['temp'].readValue() + tempReaction < tempSetPoint:
        #         self._Controller__effectors['heater'].switchOn()
        # elif self._Controller__sensors['temp'].readValue() + tempReaction > tempSetPoint:
        #     self._Controller__effectors['heater'].switchOff()
        # if self._Controller__sensors['level'].readValue() + levelReaction < levelSetPoint:
        #     if self._Controller__sensors['color'].readValue() < colourSetPoint:
        #         self._Controller__effectors['pumpB'].switchOn()
        #     else:
        #         self._Controller__effectors['pumpA'].switchOn()
        # elif self._Controller__sensors['level'].readValue() + levelReaction > levelSetPoint:
        #     self._Controller__effectors['pumpA'].switchOff()
        #     self._Controller__effectors['pumpB'].switchOff()

        # print(afstand.read_mm())
        # print(reflex.get())
        pass


# sim = Simulator(plant, Controller(), True)
# sim.run()
