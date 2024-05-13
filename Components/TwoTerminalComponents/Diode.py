from Components.allTerminalComponent import TwoTerminalComponent


class Diode(TwoTerminalComponent):
    def __init__(self, unique_id, name):
        super(Diode, self).__init__(unique_id, name)

        self.componentUnit = "kOhm"
        # self.componentName = "Diode"
        self.componentType = "Diode"
