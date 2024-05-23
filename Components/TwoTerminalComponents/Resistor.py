from Components.allTerminalComponent import TwoTerminalComponent


class Resistor(TwoTerminalComponent):
    # image_path = "../../Assets/symbols/resistor.png"
    def __init__(self, unique_id, name):
        super(Resistor, self).__init__(unique_id, name, "../Assets/symbols/resistor.png")

        self.componentUnit = "kOhm"
        # self.componentName = "Resistor"
        self.componentType = "Resistor"
        self.units = ["Ohm", "kOhm"]

        self.symbol.unit = self.componentUnit

        # self.set_unit("kOhm")
