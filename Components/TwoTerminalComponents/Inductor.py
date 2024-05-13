from Components.allTerminalComponent import TwoTerminalComponent


class Inductor(TwoTerminalComponent):
    def __init__(self, unique_id, name):
        super(Inductor, self).__init__(unique_id, name)

        self.componentUnit = "kOhm"
        # self.componentName = "Inductor"
        self.componentType = "Inductor"
