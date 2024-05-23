from Components.allTerminalComponent import TwoTerminalComponent


class DCVoltageSource(TwoTerminalComponent):
    def __init__(self, unique_id, name):
        super(DCVoltageSource, self).__init__(unique_id, name, "../Assets/symbols/DC_source.png")

        self.componentUnit = "V"
        # self.componentName = "DC Voltage Source"
        self.componentType = "Source_DC"
        self.units = ["V", "kV"]

        self.symbol.unit = self.componentUnit
        # self.symbol.image_path = "../../Assets/symbols/DC_source.png"
