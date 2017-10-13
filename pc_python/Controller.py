import lemonator

class controller:
    def __init__(self, lemonator):
        self.lemonator = lemonator()
        for x in "Hello\n":
            self.lemonator.lcd.putc(x)

    def update(self):
        if "A" == lemonator.keypad.getc() and lemonator.reflex.get():
            lemonator.sirup_valve.set(1)
            lemonator.sirup_pump.set(1)
            for x in "Pumping syrup\n":
                self.lemonator.lcd.putc(x)

            while(1):
                if lemonator.distance.read_mm() < 110 or not lemonator.reflex.get():
                    lemonator.sirup_pump.set(0)
                    lemonator.sirup_valve.set(0)
                    break

            lemonator.water_valve.set(1)
            lemonator.water_pump.set(1)
            for x in "Pumping water\n":
                self.lemonator.lcd.putc(x)

            while(1):
                if lemonator.distance.read_mm() < 90 or not lemonator.reflex.get():
                    lemonator.water_pump.set(0)
                    lemonator.water_valve.set(0)
                    break

            for x in "Finished!\n":
                self.lemonator.lcd.putc(x)
