
class proxy():

    def __init__(self, plant):
        self.plant = plant

class led_yellow():

    def __init__(self, proxy):
        self.proxy = proxy

    def set(self, c):
        if c:
            self.proxy.plant.turnon()
        else:
            self.proxy.plant.turnoff()
