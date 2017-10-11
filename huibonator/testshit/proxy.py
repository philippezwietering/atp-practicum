from sim import simulator

class proxy(simulator):

    def __init__(self, controller):
        simulator.__init__(self, controller)
        self.controller.interface = self
        self._led_yellow = led_yellow(self)

class led_yellow():

    def __init__(self, proxy):
        self.proxy = proxy

    def set(self, c):
        if c:
            self.proxy.plant.turnon()
        else:
            self.proxy.plant.turnoff()
