from Components.allTerminalComponent import TwoTerminalComponent


class PulseVoltageSource(TwoTerminalComponent):
    def __init__(self, unique_id, name):
        super(PulseVoltageSource, self).__init__(unique_id, name, "../Assets/symbols/Pulse_source.png")

        self.componentUnit = "V"
        self.initialValue = "0"
        self.pulseWidth = "10"
        self.period = "20"
        self.componentType = "Source_P"
        self.units = ["V", "kV"]

        self.symbol.unit = self.componentUnit
        # self.symbol.image_path = "../../Assets/symbols/AC_source.png"
