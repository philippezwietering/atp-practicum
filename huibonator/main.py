if __name__ == "__main__":
    """Only perform actions when invoked directly!"""
    from Simulator import Simulator
    simulator = Simulator(False) # use Simulator(False) to disable the GUI
    simulator.run()
