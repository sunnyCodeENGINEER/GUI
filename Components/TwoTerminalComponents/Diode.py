from Components.allTerminalComponent import TwoTerminalComponent


class Diode(TwoTerminalComponent):
    def __init__(self, unique_id, name):
        super(Diode, self).__init__(unique_id, name, "../Assets/symbols/diode.png")

        self.componentUnit = "kOhm"
        # self.componentName = "Diode"
        self.componentType = "Diode"
        # self.symbol.image_path = "../../Assets/symbols/diode.png"
        # self.units = {}
        self.Is = "4.35"
        self.Rs = "0.64"
        self.BV = "110"
        self.IBV = "0.0001"
        self.N = "1.906"
