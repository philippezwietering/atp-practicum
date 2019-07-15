# uncompyle6 version 3.3.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: .\Controller.py
# Size of source mod 2**32: 4002 bytes
from Effector import Effector
from Sensor import Sensor, TemperatureSensor, LevelSensor, ColourSensor, KeyPad
from Constants import *
from typing import Dict

class Controller:

    def __init__(self, sensors: Dict[(str, Sensor)], effectors: Dict[(str, Effector)]):
        """Controller is build using two Dictionaries:
        - sensors: Dict[str, Sensor], using strings 'temp', 'color', 'level'
        - effectors: Dict[str, Effector], using strings 'heater', 'pumpA', 'pumpB'
        """
        self._Controller__sensors = sensors
        self._Controller__effectors = effectors

    def update(self) -> None:
        if not self._Controller__sensors['presence'].readValue():
            self._Controller__effectors['greenM'].switchOff()
            if self._Controller__effectors['heater'].isOn() or self._Controller__effectors['pumpA'].isOn() or self._Controller__effectors['pumpB'].isOn():
                print('No cup placed; stopping all')
            self._Controller__effectors['heater'].switchOff()
            self._Controller__effectors['yellowM'].switchOff()
            self._Controller__effectors['pumpA'].switchOff()
            self._Controller__effectors['redA'].switchOff()
            self._Controller__effectors['valveA'].switchOn()
            self._Controller__effectors['greenA'].switchOn()
            self._Controller__effectors['redB'].switchOff()
            self._Controller__effectors['pumpB'].switchOff()
            self._Controller__effectors['valveB'].switchOn()
            self._Controller__effectors['greenB'].switchOn()
            return
        self._Controller__effectors['greenM'].switchOn()
        keypressed = self._Controller__sensors['keypad'].pop()
        if not keypressed == '\x00':
            print('Keypress detected!')
            if keypressed == 'A':
                print('Received an A')
                if self._Controller__effectors['pumpA'].isOn():
                    self._Controller__effectors['pumpA'].switchOff()
                    self._Controller__effectors['lcd'].pushString('\x0cPump A turned off!')
                else:
                    self._Controller__effectors['pumpA'].switchOn()
                    self._Controller__effectors['lcd'].pushString('\x0cPump A turned on!')
        if keypressed == 'B':
            print('Received an B')
            if self._Controller__effectors['pumpB'].isOn():
                self._Controller__effectors['pumpB'].switchOff()
                self._Controller__effectors['lcd'].pushString('\nPump B turned off!')
            else:
                self._Controller__effectors['pumpB'].switchOn()
                self._Controller__effectors['lcd'].pushString('\nPump B turned on!')