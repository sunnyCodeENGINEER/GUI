from Components.twoTerminalComponent import TwoTerminalComponent


class ACVoltageSource(TwoTerminalComponent):
    def __init__(self, unique_id, name):
        super(ACVoltageSource, self).__init__(unique_id, name)

        self.componentUnit = "V"
        self.componentName = "AC Voltage Source"
        self.componentType = "Active"
