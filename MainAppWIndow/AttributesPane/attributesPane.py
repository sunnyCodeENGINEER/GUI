from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QLineEdit, QComboBox, QHBoxLayout, QGraphicsView, QGraphicsScene, \
    QGraphicsItem, QPushButton
from PyQt6.sip import wrappertype

# from utils.components import QHLine
from Components.allTerminalComponent import OneTerminalComponent


class AttributesPane(QtWidgets.QWidget):
    class Signals(QtCore.QObject):
        """
        An Object class to organise all signals that would be emitted from the ComponentsPane
        """

        deleteComponent = pyqtSignal(str)

    def __init__(self, parent=None):
        # making sure that the components' pane is not any smaller than 250px
        super(AttributesPane, self).__init__(parent)
        self.setMinimumWidth(250)
        self.component = OneTerminalComponent("Ground001", "Ground-1")

        self.component_name_edit = ""
        self.value_edit = None
        self.unit_combobox = None

        # vertical box layout to arrange everything vertically
        # self.layout = QtWidgets.QVBoxLayout()
        # self.layout.setContentsMargins(5, 5, 5, 5)
        #
        # self.layout.addStretch()
        # # using the vertical box layout as the layout of the component pane
        # self.setLayout(self.layout)

        self.init_ui()

    def init_ui(self):
        # Create a QVBoxLayout to arrange widgets vertically
        layout = QVBoxLayout(self)

        # Create a QLabel for the large text
        label = QLabel("Attribute Pane", self)

        # Set font properties for the label (large text)
        font = QFont()
        font.setPointSize(20)  # Set the font size to 20 points
        font.setBold(True)  # Set the font weight to bold
        label.setFont(font)

        # Align the label to the top left
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Add the label to the layout
        layout.addWidget(label)

        # Add component preview


        # Add Component data
        component_name = QLabel("Name:")
        self.component_name_edit = QLineEdit()
        name_hbox = QHBoxLayout()
        name_hbox.addWidget(component_name)
        name_hbox.addWidget(self.component_name_edit)

        # Value
        value_label = QLabel("Value:")
        self.value_edit = QLineEdit()
        value_hbox = QHBoxLayout()
        value_hbox.addWidget(value_label)
        value_hbox.addWidget(self.value_edit)

        # Unit
        unit_label = QLabel("Unit:")
        self.unit_combobox = QComboBox()
        self.unit_combobox.addItems(["m", "cm", "mm", "inch"])
        unit_hbox = QHBoxLayout()
        unit_hbox.addWidget(unit_label)
        unit_hbox.addWidget(self.unit_combobox)

        # Action Buttons
        save_button = QPushButton("Save")
        clear_button = QPushButton("Clear")
        delete_button = QPushButton("Delete")
        action_hbox = QHBoxLayout()
        action_hbox.addWidget(save_button)
        action_hbox.addWidget(clear_button)


        # Add to layout
        preview_scene = QGraphicsView()
        scene = QGraphicsScene()
        preview_item = self.component.symbol
        preview_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        preview_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        scene.addItem(preview_item)
        preview_scene.setScene(scene)
        # preview_scene.setSceneRect(10, 10, 240, 100)
        preview_scene.setMaximumHeight(150)
        layout.addWidget(preview_scene)
        layout.addLayout(name_hbox)
        layout.addLayout(value_hbox)
        layout.addLayout(unit_hbox)
        layout.addLayout(action_hbox)
        layout.addWidget(delete_button)

        layout.addStretch()

        # Set the layout for the main widget (self)
        self.setLayout(layout)

    def on_canvas_component_select(self, component):
        self.component = component
        print("connected attribPane")

    @staticmethod
    def handle_signal(value):
        print(f"Received signal with value: {value}")

