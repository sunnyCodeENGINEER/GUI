from PyQt6.QtCore import pyqtSignal, QPointF
from PyQt6.QtWidgets import QGraphicsObject

from Components.symbol import Symbol
from Components.symbolWithOneTerminal import SymbolWithOneTerminal
from Components.symbolWithThreeTerminals import SymbolWithThreeTerminals
from Components.symbolWithTwoTerminals import SymbolWithTwoTerminals


class OneTerminalComponent:
    # self.componentID = ""
    # self.componentType = ""
    # self.component_name = ""
    # self.componentValue = ""
    # self.componentUnit = ""
    # self.terminal1To = ""
    # self.terminal2To = ""

    class Signals(QGraphicsObject):
        terminalClicked = pyqtSignal(str, QPointF, int)
        componentMoved = pyqtSignal(QPointF)
        componentSelected = pyqtSignal(str)
        componentDeselected = pyqtSignal()
        componentDataChanged = pyqtSignal()

    def __init__(self, unique_id, name):
        self.componentID = unique_id
        self.componentName = name
        self.componentType = ""
        self.componentValue = "0"
        self.componentUnit = ""
        self.terminal1To = ""

        self.symbol = SymbolWithOneTerminal(name)

        # set signals
        self.signals = self.Signals()

        self.symbol.signals.terminalClicked.connect(self.terminal_clicked)
        self.symbol.signals.componentSelected.connect(self.component_clicked)
        self.symbol.signals.componentDeselected.connect(self.component_deselected)
        self.symbol.signals.componentMoved.connect(self.component_moved)

    def set_value(self, value):
        self.componentValue = value

    def set_unit(self, unit):
        self.componentUnit = unit

    def set_terminal_1_to(self, connected_to):
        self.terminal1To = connected_to

    def terminal_clicked(self, point, unique_id):
        # handle terminal selection on symbol
        self.signals.terminalClicked.emit(self.componentID, point, unique_id)
        print("I worked")
        print(f"Received QPointF: ({point.x()}, {point.y()})\nTerminal ID: {unique_id}")

    def component_clicked(self):
        print("\n\tclicked")
        print(self.terminal1To)
        self.signals.componentSelected.emit(self.componentID)

    def component_deselected(self):
        self.signals.componentDeselected.emit()
        self.symbol.reset_terminals()

    def component_moved(self, offset):
        self.signals.componentMoved.emit(offset)

    def reset_terminal(self):
        self.symbol.reset_terminals()


class TwoTerminalComponent(OneTerminalComponent):
    def __init__(self, unique_id, name):
        super(TwoTerminalComponent, self).__init__(unique_id, name)
        self.terminal2To = ""
        self.symbol = SymbolWithTwoTerminals(name)

        # self.signals.terminalClicked.connect(self.terminal_clicked())
        self.symbol.signals.terminalClicked.connect(self.terminal_clicked)
        self.symbol.signals.componentSelected.connect(self.component_clicked)
        self.symbol.signals.componentDeselected.connect(self.component_deselected)
        self.symbol.signals.componentMoved.connect(self.component_moved)

    def set_terminal_2_to(self, connected_to):
        self.terminal2To = connected_to

    def terminal_clicked(self, point, unique_id):
        self.signals.terminalClicked.emit(self.componentID, point, unique_id)

    def component_clicked(self):
        print(f"\n\nterminal 1 to : {self.terminal1To}")
        print(f"terminal 2 to : {self.terminal2To}")
        self.signals.componentSelected.emit(self.componentID)

    def component_deselected(self):
        self.signals.componentDeselected.emit()
        self.symbol.reset_terminals()

    def component_moved(self, offset):
        self.signals.componentMoved.emit(offset)

    def reset_terminal(self):
        self.symbol.reset_terminals()


class ThreeTerminalComponent(OneTerminalComponent):
    def __init__(self, unique_id, name):
        super(ThreeTerminalComponent, self).__init__(unique_id, name)
        self.terminal2To = ""
        self.terminal3To = ""
        self.symbol = SymbolWithThreeTerminals(name)

        # connect signal emitted from symbol to component model
        self.symbol.signals.terminalClicked.connect(self.terminal_clicked)
        self.symbol.signals.componentSelected.connect(self.component_clicked)
        self.symbol.signals.componentDeselected.connect(self.component_deselected)
        self.symbol.signals.componentMoved.connect(self.component_moved)

    def set_terminal_2_to(self, connected_to):
        self.terminal2To = connected_to

    def set_terminal_3_to(self, connected_to):
        self.terminal3To = connected_to

    def terminal_clicked(self, point, unique_id):
        # handle terminal selection on symbol
        self.signals.terminalClicked.emit(self.componentID, point, unique_id)

    def component_clicked(self):
        self.signals.componentSelected.emit(self.componentID)

    def component_deselected(self):
        self.signals.componentDeselected.emit()
        self.symbol.reset_terminals()

    def component_moved(self, offset):
        self.signals.componentMoved.emit(offset)

    def reset_terminal(self):
        self.symbol.reset_terminals()
