from Components.allTerminalComponent import TwoTerminalComponent


class Capacitor(TwoTerminalComponent):
    def __init__(self, unique_id, name):
        super(Capacitor, self).__init__(unique_id, name, "../../Assets/symbols/capacitor.png")

        self.componentUnit = "uF"
        # self.componentName = "Capacitor"
        self.componentType = "Capacitor"
        self.units = ["uF", "F"]

        self.symbol.unit = self.componentUnit
        self.symbol.image_path = "../Assets/symbols/capacitor.png"

        