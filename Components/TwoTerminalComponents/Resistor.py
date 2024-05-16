from Components.allTerminalComponent import TwoTerminalComponent


class Resistor(TwoTerminalComponent):
    def __init__(self, unique_id, name):
        super(Resistor, self).__init__(unique_id, name)

        self.componentUnit = "kOhm"
        # self.componentName = "Resistor"
        self.componentType = "Resistor"
        self.units = ["Ohm", "kOhm"]
