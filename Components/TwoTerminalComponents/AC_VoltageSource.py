from Components.allTerminalComponent import TwoTerminalComponent


class ACVoltageSource(TwoTerminalComponent):
    def __init__(self, unique_id, name):
        super(ACVoltageSource, self).__init__(unique_id, name, "../Assets/symbols/AC_source.png")

        self.componentUnit = "V"
        self.frequency = "100"
        # self.componentName = "AC Voltage Source"
        self.componentType = "Source_AC"
        self.units = ["V", "kV"]

        self.symbol.unit = self.componentUnit
        # self.symbol.image_path = "../../Assets/symbols/AC_source.png"
