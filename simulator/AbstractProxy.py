# This file is necessary for mocking the proxy. 
# It doesn't really add functionality on its own, but only checks for implementation of functions

from abc import ABC, abstractmethod

class AbstractProxy:

    class Effector(ABC):
        @abstractmethod
        def switchOn(self) -> None:
            raise NotImplementedError("Method switchOn is not implemented")
        
        @abstractmethod
        def switchOff(self) -> None:
            raise NotImplementedError("Method switchOff is not implemented")
        
        @abstractmethod
        def isOn(self) -> bool:
            raise NotImplementedError("Method isOn is not implemented")
        
        @abstractmethod
        def update(self) -> None:
            raise NotImplementedError("Method update is not implemented")

    class Valve(Effector):
        @abstractmethod
        def setPump(self, pump) -> None:
            raise NotImplementedError("Method setPump is not implemented")

    class Pump(Effector):
        pass
    
    class Heater(Effector):
        pass

    class Led(Effector):
        @abstractmethod
        def getColour(self):
            raise NotImplementedError("Method getColour is not implemented")

        @abstractmethod
        def toggle(self) -> None:
            raise NotImplementedError("Method toggle is not implemented")

    class Lcd(Effector):
        @abstractmethod
        def getLines(self) -> str:
            raise NotImplementedError("Method getLines is not implemented")

        @abstractmethod
        def pushString(self, s: str) -> None:
            raise NotImplementedError("Method pushString is not implemented")

        @abstractmethod
        def put(self, s: str) -> None:
            raise NotImplementedError("Method put is not implemented")

        @abstractmethod
        def clear(self) -> None:
            raise NotImplementedError("Method clear is not implemented")

    class Sensor(ABC):
        @abstractmethod
        def update(self) -> None:
            raise NotImplementedError("Method update is not implemented")

        @abstractmethod
        def readValue(self) -> float:
            raise NotImplementedError("Method readValues is not implemented")
        
        @abstractmethod
        def measure(self) -> str:
            raise NotImplementedError("Method measure is not implemented")

        @abstractmethod
        def _convertToValue(self) -> float:
            raise NotImplementedError("Method _convertToValue is not implemented")

    class presenceSensor(Sensor):
        pass

    class colourSensor(Sensor):
        pass
    
    class levelSensor(Sensor):
        pass
    
    class temperatureSensor(Sensor):
        pass

    class keyPad(Sensor):
        @abstractmethod
        def push(self, c: str) -> None:
            raise NotImplementedError("Method push is not implemented")
        
        @abstractmethod
        def pop(self) -> str:
            raise NotImplementedError("Method pop is not implemented")