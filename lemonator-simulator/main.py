if __name__ == "__main__":
    """Only perform actions when invoked directly!"""
    from Simulator import *
    from Controller import *
    simulator = Simulator(Plant(), Controller(), True) # use Simulator(False) to disable the GUI
    simulator.run()
