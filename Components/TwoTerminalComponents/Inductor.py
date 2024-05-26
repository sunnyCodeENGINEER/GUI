from Components.allTerminalComponent import TwoTerminalComponent



class Inductor(TwoTerminalComponent):
    def __init__(self, unique_id, name):
        super(Inductor, self).__init__(unique_id, name, "../Assets/symbols/inductor.png")

        self.componentUnit = "H"
        # self.componentName = "Inductor"
        self.componentType = "Inductor"
        self.units = ["H"]
        # self.units = {}


        self.symbol.unit = self.componentUnit
