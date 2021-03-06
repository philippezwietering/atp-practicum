import cppimport.import_hook
import argparse

import Simulator
import CustomController
import CPPController
import Gui
import SimProxy

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lemonator")
    parser.add_argument("--py", help="Run the lemonator with the python controller", action="store_true")
    parser.add_argument("--cpp", help="Run the lemonator with the cpp controller", action="store_true")
    args = parser.parse_args()

    if args.py and args.cpp:
        print("You can't run both controllers simultaneously, please choose one")
        exit()
    
    simulator = Simulator.Simulator(False) # use Simulator(False) to disable the GUI
    proxy = SimProxy.SimProxy

    # Effectors
    pumpA = proxy.Pump(simulator._Simulator__plant._effectors['pumpA'])
    pumpB = proxy.Pump(simulator._Simulator__plant._effectors['pumpB'])
    valveA = proxy.Valve(simulator._Simulator__plant._effectors['valveA'])
    valveB = proxy.Valve(simulator._Simulator__plant._effectors['valveB'])
    heater = proxy.Heater(simulator._Simulator__plant._effectors['heater'])

    # LEDs
    ledRedA = proxy.Led(simulator._Simulator__plant._effectors['redA'])
    ledGreenA = proxy.Led(simulator._Simulator__plant._effectors['greenA'])
    ledRedB = proxy.Led(simulator._Simulator__plant._effectors['redB'])
    ledGreenB = proxy.Led(simulator._Simulator__plant._effectors['greenB'])
    ledGreenM = proxy.Led(simulator._Simulator__plant._effectors['greenM'])
    ledYellowM = proxy.Led(simulator._Simulator__plant._effectors['yellowM'])

    # Sensors
    colour = proxy.colourSensor(simulator._Simulator__plant._sensors['colour'])
    temperature = proxy.temperatureSensor(simulator._Simulator__plant._sensors['temp'])
    level = proxy.levelSensor(simulator._Simulator__plant._sensors['level'])
    presence = proxy.presenceSensor(simulator._Simulator__plant._sensors['presence'])

    # User objects
    keypad = proxy.keyPad(simulator._Simulator__plant._sensors['keypad'])
    lcd = proxy.Lcd(simulator._Simulator__plant._effectors['lcd'])

    controller = None

    if args.cpp:
        controller = CPPController.Controller(pumpA, pumpB, valveA, valveB, ledRedA, ledGreenA, ledRedB, ledGreenB, ledGreenM, ledYellowM, heater, temperature, level, presence, colour, keypad, lcd)

    else:
        controller = CustomController.Controller(pumpA, pumpB, valveA, valveB, ledRedA, ledGreenA, ledRedB, ledGreenB, ledGreenM, ledYellowM, heater, temperature, level, presence, colour, keypad, lcd)    
    
    controller.initialize()

    simulator._Simulator__controller = controller
    simulator._Simulator__gui = Gui.GUI(simulator._Simulator__plant, controller, simulator._Simulator__monitor)
    simulator.run()