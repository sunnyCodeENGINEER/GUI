from functools import partial

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QLineEdit, QComboBox, QHBoxLayout, QPushButton, QVBoxLayout
from PyQt6.sip import wrappertype

# from utils.components import QHLine
from Components.OneTerminalComponents.Ground import Ground
from Components.ThreeTerminalComponents.TestTransistor import TestTransistor
from Components.TwoTerminalComponents.AC_VoltageSource import ACVoltageSource
from Components.TwoTerminalComponents.Capacitor import Capacitor
from Components.TwoTerminalComponents.DC_VoltageSource import DCVoltageSource
from Components.TwoTerminalComponents.Inductor import Inductor
from Components.TwoTerminalComponents.Resistor import Resistor
from Components.allTerminalComponent import OneTerminalComponent, TwoTerminalComponent


class ComponentsPane(QtWidgets.QWidget):
    # class Signals(QtCore.QObject):
    #     """
    #     An Object class to organise all signals that would be emitted from the ComponentsPane
    #     """
    #
    #     componentSelected = QtCore.pyqtSignal(OneTerminalComponent)
    #
    # def __init__(self, parent=None):
    #     super(ComponentsPane, self).__init__(parent)
    #     # making sure that the components' pane is not any smaller than 250px
    #     self.setMinimumWidth(250)
    #     # vertical box layout to arrange everything vertically
    #     self.layout = QtWidgets.QVBoxLayout()
    #     self.layout.setContentsMargins(5, 5, 5, 5)
    #
    #     # Create a QLabel for the large text
    #     label = QLabel("Component Pane", self)
    #     # Set font properties for the label (large text)
    #     font = QFont()
    #     font.setPointSize(20)  # Set the font size to 20 points
    #     font.setBold(True)  # Set the font weight to bold
    #     label.setFont(font)
    #     # Align the label to the top left
    #     label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    #     # Add the label to the layout
    #     self.layout.addWidget(label)
    #
    #     # add search box to the top of the components list
    #     self.searchBox = QtWidgets.QLineEdit()
    #     self.searchBox.setPlaceholderText("Search component or category")
    #     # self.searchBox.textChanged.connect(self.onSearchBoxTextChange)
    #     self.layout.addWidget(self.searchBox)
    #     self.layout.setAlignment(self.searchBox, QtCore.Qt.AlignmentFlag.AlignTop)
    #
    #     # add a line separator between the search bar and the rest
    #     # self.layout.addWidget(QHLine())
    #
    #     # creating a dropdown menu used to select component category
    #     self.componentCategory = QtWidgets.QComboBox()
    #     self.componentCategory.setPlaceholderText("Choose a component category")
    #     # sets the initial state of the components' category to "All" to display all components from the start
    #     self.componentCategory.setCurrentText("All")
    #
    #     # List of all components
    #     self.init_components()
    #
    #     # adding stretch to the bottom to push all the components up
    #     self.layout.addStretch()
    #     # using the vertical box layout as the layout of the component pane
    #     self.setLayout(self.layout)
    #
    #     self.signals = self.Signals()
    #     self.component: OneTerminalComponent = Resistor("Resistor-00", "Resistor-00")
    #
    # def init_components(self):
    #     button_labels = [
    #         "Resistor", "Voltage Source (DC)", "Ground", "Capacitor", "Inductor",
    #         "Voltage Source (AC)"
    #     ]
    #     button_labels.sort()
    #
    #     component_list = QVBoxLayout()
    #     component_list.setSpacing(1)
    #
    #     # for label in button_labels:
    #     #     button = QPushButton(label, self)
    #     #     button.setStyleSheet("text-align: left;")
    #     #     button.clicked.connect(partial(self.generate_component, label))
    #
    #     for label in button_labels:
    #         button = QLabel(label)
    #         button.setStyleSheet("text-align: left;")
    #         button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    #         button.mousePressEvent = self.on_component_click(label)
    #
    #         component_list.addWidget(button)
    #
    #     self.layout.addLayout(component_list)
    #
    # def on_component_click(self, label):
    #     """
    #     This function creates and returns the handler functions for each component that is displayed on components pane
    #     It handler function is customized based on component to make sure that the right component calsses are emitted when clicked on
    #     """
    #     component = self.generate_component_from_label(label)
    #
    #     def onComponentClick(event):
    #         self.signals.componentSelected.emit(component)
    #         print("success")
    #
    #     return onComponentClick
    #
    # def on_component_click(self, component):
    #     try:
    #         self.signals.componentSelected.emit(component)  # emit component that will be added to the canvas
    #         print("successful")
    #     except Exception as e:
    #         # Handle any other exceptions
    #         print(f"An error occurred: {e}")
    #
    #     # print(component.componentID)
    #
    # def generate_component(self, component_type):
    #     # component = None
    #     if component_type == "Resistor":
    #         self.component = Resistor("Resistor-0", "Resistor-0")
    #         self.on_component_click(self.component)
    #         # self.signals.componentSelected.emit(self.component)
    #         # return self.component
    #     elif component_type == "Voltage Source (DC)":
    #         self.component = DCVoltageSource("Source_DC-0", "Source_DC-0")
    #         self.on_component_click(self.component)
    #         # return self.component
    #     elif component_type == "Ground":
    #         self.component = Ground("Ground-0", "Ground-0")
    #         self.on_component_click(self.component)
    #         # return self.component
    #     elif component_type == "Capacitor":
    #         self.component = Capacitor("Capacitor-0", "Capacitor-0")
    #         self.on_component_click(self.component)
    #         # return self.component
    #     elif component_type == "Inductor":
    #         self.component = Inductor("Inductor-0", "Inductor-0")
    #         self.on_component_click(self.component)
    #         # return self.component
    #     elif component_type == "Voltage Source (AC)":
    #         self.component = ACVoltageSource("Source_AC-0", "Source_AC-0")
    #         self.on_component_click(self.component)
    #         # return self.component
    #
    # def generate_component_from_label(self, component_type):
    #     component = None
    #     if component_type == "Resistor":
    #         component = Resistor("Resistor-0", "Resistor-0")
    #         # return component
    #     elif component_type == "Voltage Source (DC)":
    #         component = DCVoltageSource("Source_DC-0", "Source_DC-0")
    #         # return component
    #     elif component_type == "Ground":
    #         component = Ground("Ground-0", "Ground-0")
    #         # return component
    #     elif component_type == "Capacitor":
    #         component = Capacitor("Capacitor-0", "Capacitor-0")
    #         # return component
    #     elif component_type == "Inductor":
    #         component = Inductor("Inductor-0", "Inductor-0")
    #         # return component
    #     elif component_type == "Voltage Source (AC)":
    #         component = ACVoltageSource("Source_AC-0", "Source_AC-0")
    #         # return component
    #
    #     return component

    class Signals(QtCore.QObject):
        componentSelected = QtCore.pyqtSignal(OneTerminalComponent)

    def __init__(self, parent=None):
        super(ComponentsPane, self).__init__(parent)
        self.setMinimumWidth(250)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)

        label = QLabel("Component Pane", self)
        font = label.font()
        font.setPointSize(20)
        font.setBold(True)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(label)

        self.searchBox = QtWidgets.QLineEdit()
        self.searchBox.setPlaceholderText("Search component or category")
        self.layout.addWidget(self.searchBox)

        self.componentCategory = QtWidgets.QComboBox()
        self.componentCategory.setPlaceholderText("Choose a component category")
        self.componentCategory.setCurrentText("All")

        self.init_components()

        self.layout.addStretch()
        self.setLayout(self.layout)

        self.signals = self.Signals()  # Initialize custom signals object
        # self.signals.componentSelected.connect(self.handle_component_selected)

    def init_components(self):
        button_labels = [
            "Resistor", "Voltage Source (DC)", "Ground", "Capacitor", "Inductor", "Voltage Source (AC)",\
            "Test Transistor"
        ]
        button_labels.sort()

        component_list = QVBoxLayout()
        component_list.setSpacing(1)

        for label in button_labels:
            button = QLabel(label)
            button.setStyleSheet("text-align: left;")
            button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            button.mousePressEvent = lambda event, label=label: self.on_component_click(label)
            component_list.addWidget(button)

        self.layout.addLayout(component_list)

    def on_component_click(self, component_type):
        component = self.generate_component_from_label(self, component_type)
        if component is not None:
            self.signals.componentSelected.emit(component)

            # print("Component selected:", component.componentID)

    # def handle_component_selected(self, component):
    #     print(f"Component selected: {component.componentID}!!!")

    @staticmethod
    def generate_component_from_label(self, component_type):
        component = None
        if component_type == "Resistor":
            component = Resistor("Resistor-", "Resistor-")
        elif component_type == "Voltage Source (DC)":
            component = DCVoltageSource("Source_DC-", "Source_DC-")
        elif component_type == "Ground":
            component = Ground("Ground-", "Ground-")
        elif component_type == "Capacitor":
            component = Capacitor("Capacitor-", "Capacitor-")
        elif component_type == "Inductor":
            component = Inductor("Inductor-", "Inductor-")
        elif component_type == "Voltage Source (AC)":
            component = ACVoltageSource("Source_AC-", "Source_AC-")
        elif component_type == "Test Transistor":
            component = TestTransistor("test_transist-", "test_transist-")
        return component

