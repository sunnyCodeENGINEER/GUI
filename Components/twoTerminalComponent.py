from Components.symbol import Symbol
from Components.symbolWithThreeTerminals import SymbolWithThreeTerminals
from Components.symbolWithTwoTerminals import SymbolWithTwoTerminals


class Component:
    # self.componentID = ""
    # self.componentType = ""
    # self.componentName = ""
    # self.componentValue = ""
    # self.componentUnit = ""
    # self.terminal1To = ""
    # self.terminal2To = ""

    def __init__(self, unique_id, name):
        self.componentID = unique_id
        self.componentName = name
        self.componentType = ""
        self.componentValue = 0
        self.componentUnit = ""
        self.terminal1To = ""

    def set_value(self, value):
        self.componentValue = value

    def set_unit(self, unit):
        self.componentUnit = unit

    def set_terminal_1_to(self, connected_to):
        self.terminal1To = connected_to

    # def set_terminal_2_to(self, connected_to):
    #     self.terminal2To = connected_to


class TwoTerminalComponent(Component):
    def __init__(self, unique_id, name):
        super(TwoTerminalComponent, self).__init__(unique_id, name)
        self.terminal2To = ""
        self.symbol = SymbolWithTwoTerminals()

    def set_terminal_2_to(self, connected_to):
        self.terminal2To = connected_to


class ThreeTerminalComponent(Component):
    def __init__(self, unique_id, name):
        super(ThreeTerminalComponent, self).__init__(unique_id, name)
        self.terminal2To = ""
        self.terminal3To = ""
        self.symbol = SymbolWithThreeTerminals()

    def set_terminal_2_to(self, connected_to):
        self.terminal2To = connected_to
