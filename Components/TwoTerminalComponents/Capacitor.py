from Components.allTerminalComponent import TwoTerminalComponent


class Capacitor(TwoTerminalComponent):
    def __init__(self, unique_id, name):
        super(Capacitor, self).__init__(unique_id, name, "../../Assets/symbols/capacitor.png")

        self.componentUnit = "kOhm"
        # self.componentName = "Capacitor"
        self.componentType = "Capacitor"

        self.symbol.unit = self.componentUnit
        self.symbol.image_path = "../Assets/symbols/capacitor.png"

        