from Components.symbol import Symbol


class Component:
    # self.componentID = ""
    # self.componentType = ""
    # self.componentName = ""
    # self.componentValue = ""
    # self.componentUnit = ""
    # self.terminal1To = ""
    # self.terminal2To = ""

    def __init__(self, id, name):
        self.componentID = id
        self.componentName = name
        self.componentType = ""
        self.componentValue = ""
        self.componentUnit = ""
        self.terminal1To = ""
        self.terminal2To = ""
        self.symbol = Symbol()

    def set_value(self, value):
        self.componentValue = value

    def set_unit(self, unit):
        self.componentUnit = unit

    def set_terminal_1_to(self, connected_to):
        self.terminal1To = connected_to

    def set_terminal_2_to(self, connected_to):
        self.terminal2To = connected_to
