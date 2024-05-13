from Components.allTerminalComponent import TwoTerminalComponent


class DCVoltageSource(TwoTerminalComponent):
    def __init__(self, unique_id, name):
        super(DCVoltageSource, self).__init__(unique_id, name)

        self.componentUnit = "V"
        # self.componentName = "DC Voltage Source"
        self.componentType = "Source_DC"
