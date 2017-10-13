class plant:

    def __init__(self):
        self.bool = False

    def turnon(self):
        self.bool = True

    def turnoff(self):
        self.bool = False

    def check(self):
        return self.bool


class simulator:

    def __init__(self, plant, controller):
        self.plant = plant
        self.controller = controller

    def run(self):
        for i in range(3):
            self.controller.update()
