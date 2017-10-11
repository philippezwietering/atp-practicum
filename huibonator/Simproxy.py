from Effector import Effector
from Sensor import Sensor, TemperatureSensor, LevelSensor, ColourSensor
from Constants import *
from typing import Dict
from time import sleep

class lemonator:

    def __init__(self, sensors: Dict[str, Sensor],
                 effectors: Dict[str, Effector]):
        """Controller is build using two Dictionaries:
        - sensors: Dict[str, Sensor], using strings 'temp', 'color', 'level'
        - effectors: Dict[str, Effector], using strings 'heater', 'pumpA', 'pumpB'
        """
        self._SimProxy__sensors = sensors
        self._SimProxy__effectors = effectors

    class led_yellow(lemonator):

        def set(c: bool):
            if c:
                self.SimProxy__sensors["led_yellow"].switchOn()
            else:
                self.SimProxy__sensors["led_yellow"].switchOff()
