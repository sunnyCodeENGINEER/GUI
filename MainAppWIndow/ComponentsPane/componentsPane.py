from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QLineEdit, QComboBox, QHBoxLayout, QPushButton, QVBoxLayout
from PyQt6.sip import wrappertype


# from utils.components import QHLine


class ComponentsPane(QtWidgets.QWidget):
    class Signals(QtCore.QObject):
        """
        An Object class to organise all signals that would be emitted from the ComponentsPane
        """

        componentSelected = QtCore.pyqtSignal(wrappertype)

    def __init__(self, parent=None):
        super(ComponentsPane, self).__init__(parent)

        # making sure that the components' pane is not any smaller than 250px
        self.setMinimumWidth(250)

        # vertical box layout to arrange everything vertically
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)

        # Create a QLabel for the large text
        label = QLabel("Component Pane", self)

        # Set font properties for the label (large text)
        font = QFont()
        font.setPointSize(20)  # Set the font size to 20 points
        font.setBold(True)  # Set the font weight to bold
        label.setFont(font)

        # Align the label to the top left
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Add the label to the layout
        self.layout.addWidget(label)

        # add search box to the top of the components list
        self.searchBox = QtWidgets.QLineEdit()
        self.searchBox.setPlaceholderText("Search component or category")
        # self.searchBox.textChanged.connect(self.onSearchBoxTextChange)
        self.layout.addWidget(self.searchBox)
        self.layout.setAlignment(self.searchBox, QtCore.Qt.AlignmentFlag.AlignTop)

        # add a line separator between the search bar and the rest
        # self.layout.addWidget(QHLine())

        # creating a dropdown menu used to select component category
        self.componentCategory = QtWidgets.QComboBox()
        self.componentCategory.setPlaceholderText("Choose a component category")

        # sets the initial state of the components' category to "All" to display all components from the start
        self.componentCategory.setCurrentText("All")

        # List of all components
        self.init_components()

        # adding stretch to the bottom to push all the components up
        self.layout.addStretch()
        # using the vertical box layout as the layout of the component pane
        self.setLayout(self.layout)

        self.signals = self.Signals()

    def init_components(self):
        button_labels = [
            "Resistor", "Voltage Source (DC)", "Ground", "Capacitor", "Inductor",
            "Voltage Source"
        ]

        component_list = QVBoxLayout()
        component_list.setSpacing(1)

        for label in button_labels:
            button = QPushButton(label, self)
            button.setStyleSheet("text-align: left;")
            component_list.addWidget(button)

        self.layout.addLayout(component_list)

    def on_component_click(self, component):
        self.signals.componentSelected.emit(component)  # emit component that will be added to the canvas
