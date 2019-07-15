# This file is usable as a proxy to the plant interface, so stuff can be tested outside of the Lemonator system itself
# It takes either an effector or sensor so it can be used to call functions on it, precisely like a proxy :)
# Every method of all the different effectors and sensors should be covered in here

from AbstractProxy import AbstractProxy

class SimProxy(AbstractProxy):
    class Effector(AbstractProxy.Effector):
        def __init__(self, effector):
            self.effector = effector

        def switchOn(self) -> None:
            self.effector.switchOn()
        
        def switchOff(self) -> None:
            self.effector.switchOff()
        
        def isOn(self) -> bool:
            return self.effector.isOn()
        
        def update(self) -> None:
            self.effector.update()

    class Valve(AbstractProxy.Valve, Effector):
        def setPump(self, pump) -> None:
            self.effector.setPump(pump)

    class Pump(AbstractProxy.Pump, Effector):
        pass
    
    class Heater(AbstractProxy.Heater, Effector):
        pass

    class Led(AbstractProxy.Led, Effector):
        def getColour(self):
            return self.effector.getColour()

        def toggle(self) -> None:
            self.effector.toggle()

    class Lcd(AbstractProxy.Lcd, Effector):
        def getLines(self) -> str:
            return self.effector.getLines()

        def pushString(self, s: str) -> None:
            self.effector.pushString(s)

        def put(self, s: str) -> None:
            self.effector.put(s)

        def clear(self) -> None:
            self.effector.clear()

    class Sensor(AbstractProxy.Sensor):
        def __init__(self, sensor):
            self.sensor = sensor

        def update(self) -> None:
            self.sensor.update()

        def readValue(self) -> float:
            return self.sensor.readValue()
        
        def measure(self) -> str:
            return self.sensor.measure()

        def _convertToValue(self) -> float:
            return self.sensor._convertToValue()

    class presenceSensor(AbstractProxy.presenceSensor, Sensor):
        pass

    class colourSensor(AbstractProxy.colourSensor, Sensor):
        pass
    
    class levelSensor(AbstractProxy.levelSensor, Sensor):
        pass
    
    class temperatureSensor(AbstractProxy.temperatureSensor, Sensor):
        pass

    class keyPad(AbstractProxy.keyPad, Sensor):
        def push(self, c: str) -> None:
            self.sensor.push(c)
        
        def pop(self) -> str:
            return self.sensor.pop()

# class StubLemonator:

#     def __init__(self):
#         self.led_yellow = SimProxy.Led()
#         self.led_green = SimProxy.Led()
#         self.water_pump = SimProxy.Pump()
#         self.sirup_pump = SimProxy.Pump()
#         self.water_valve = SimProxy.Valve()
#         self.sirup_valve = SimProxy.Valve()
#         self.heater = SimProxy.Heater()
#         self.colour = SimProxy.colourSensor()
#         self.distance = SimProxy.levelSensor()
#         self.reflex = SimProxy.presenceSensor()
#         self.lcd = SimProxy().Lcd()
#         self.keypad = SimProxy.keyPad()