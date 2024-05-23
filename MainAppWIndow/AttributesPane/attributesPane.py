from copy import copy

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QLineEdit, QComboBox, QHBoxLayout, QGraphicsView, QGraphicsScene, \
    QGraphicsItem, QPushButton, QMessageBox
from PyQt6.sip import wrappertype

# from utils.components import QHLine
from Components.OneTerminalComponents.Ground import Ground
from Components.allTerminalComponent import OneTerminalComponent


class AttributesPane(QtWidgets.QWidget):
    class Signals(QtCore.QObject):
        """
        An Object class to organise all signals that would be emitted from the ComponentsPane
        """

        deleteComponent = pyqtSignal(str)
        deleteWire = pyqtSignal(str)

    class DeleteConfirmationDialog(QMessageBox):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setIcon(QMessageBox.Icon.Warning)
            self.setWindowTitle("Confirm Deletion")
            self.setText("Are you sure you want to delete this item?")
            self.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            self.setDefaultButton(QMessageBox.StandardButton.No)

    def delete_item(self):
        # Instantiate the confirmation dialog
        confirmation_dialog = self.DeleteConfirmationDialog()

        # Execute the dialog and capture the result
        result = confirmation_dialog.exec()

        # Check the result and perform delete action if confirmed
        if result == QMessageBox.StandardButton.Yes:
            # Perform delete operation here
            self.on_delete()
            print("Delete confirmed")
        else:
            print("Delete canceled")

    def delete_wire(self):
        # Instantiate the confirmation dialog
        confirmation_dialog = self.DeleteConfirmationDialog()

        # Execute the dialog and capture the result
        result = confirmation_dialog.exec()

        # Check the result and perform delete action if confirmed
        if result == QMessageBox.StandardButton.Yes:
            # Perform delete operation here
            self.on_wire_delete()
            print("Delete confirmed")
        else:
            print("Delete canceled")

    def __init__(self, parent=None):
        # making sure that the components' pane is not any smaller than 250px
        super(AttributesPane, self).__init__(parent)
        self.setMinimumWidth(250)
        # self.component = Ground("Ground-", "Ground-")
        self.component = None
        self.wire = None

        self.wire_name_edit = QLineEdit()
        self.value_edit = QLineEdit()
        self.attribute1 = QLineEdit()
        self.attribute2 = QLineEdit()
        self.attribute3 = QLineEdit()
        self.attribute4 = QLineEdit()
        self.attribute5 = QLineEdit()
        self.attribute6 = QLineEdit()
        self.attribute7 = QLineEdit()
        self.attribute8 = QLineEdit()
        self.attribute9 = QLineEdit()
        self.unit_combobox = QComboBox()

        self.component_data_label = QLabel()

        self.layout = QVBoxLayout(self)

        self.init_ui()

        self.signals = self.Signals()

    def init_ui(self):
        with open("../Assets/styles/attributes_pane.stylesheet.qss", "r") as f:
            style_sheet = f.read()
            self.setStyleSheet(style_sheet)
        # Create a QVBoxLayout to arrange widgets vertically
        layout = QVBoxLayout(self)

        # Create a QLabel for the large text
        label = QLabel("Attribute Pane", self)

        # Set font properties for the label (large text)
        font = QFont()
        font.setPointSize(15)  # Set the font size to 20 points
        font.setBold(True)  # Set the font weight to bold
        label.setFont(font)

        # Align the label to the top left
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Add the label to the layout
        self.layout.addWidget(label)

        # # Add component preview
        #
        #
        # # Add Component data
        # component_name = QLabel("Name:")
        # self.wire_name_edit = QLineEdit()
        # name_hbox = QHBoxLayout()
        # name_hbox.addWidget(component_name)
        # name_hbox.addWidget(self.wire_name_edit)
        #
        # # Value
        # value_label = QLabel("Value:")
        # self.value_edit = QLineEdit()
        # value_hbox = QHBoxLayout()
        # value_hbox.addWidget(value_label)
        # value_hbox.addWidget(self.value_edit)
        #
        # # Unit
        # unit_label = QLabel("Unit:")
        # self.unit_combobox = QComboBox()
        # self.unit_combobox.addItems(["m", "cm", "mm", "inch"])
        # unit_hbox = QHBoxLayout()
        # unit_hbox.addWidget(unit_label)
        # unit_hbox.addWidget(self.unit_combobox)
        #
        # # Action Buttons
        # save_button = QPushButton("Save")
        # clear_button = QPushButton("Clear")
        # delete_button = QPushButton("Delete")
        # action_hbox = QHBoxLayout()
        # action_hbox.addWidget(save_button)
        # action_hbox.addWidget(clear_button)
        #
        #
        # # Add to layout
        # preview_scene = QGraphicsView()
        # scene = QGraphicsScene()
        # preview_item = self.component.symbol
        # preview_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        # preview_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        # scene.addItem(preview_item)
        # preview_scene.setScene(scene)
        # # preview_scene.setSceneRect(10, 10, 240, 100)
        # preview_scene.setMaximumHeight(150)
        # layout.addWidget(preview_scene)
        # layout.addLayout(name_hbox)
        # layout.addLayout(value_hbox)
        # layout.addLayout(unit_hbox)
        # layout.addLayout(action_hbox)
        # layout.addWidget(delete_button)

        if self.component is not None:
            self.component_data(self.layout)

        if self.wire is not None:
            self.wire_data(self.layout)

        if self.component is None and self.wire is None:
            self.no_component_selected(self.layout)
        # else:
        #     self.component_data_label.setText("No Component Selected")
        #     self.layout.addWidget(self.component_data_label)

        self.layout.addStretch()

        # Set the layout for the main widget (self)
        self.setLayout(self.layout)

    def component_data(self, layout):
        # Create a QLabel for the large text
        label = QLabel(f"Component Type: {self.component.componentType.upper()}", self)

        # Set font properties for the label (large text)
        font = QFont()
        font.setPointSize(9)  # Set the font size to 20 points
        font.setBold(True)  # Set the font weight to bold
        label.setFont(font)

        # Align the label to the top left
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Add the label to the layout
        layout.addWidget(label)
        # Add Component data
        component_name = QLabel("Name:")
        self.wire_name_edit = QLineEdit(self)
        self.wire_name_edit.setText(self.component.componentName)
        name_hbox = QHBoxLayout()
        name_hbox.addWidget(component_name)
        name_hbox.addWidget(self.wire_name_edit)

        # Value
        value_label = QLabel("Value:")
        self.value_edit = QLineEdit(self)
        self.value_edit.setText(self.component.componentValue)
        value_hbox = QHBoxLayout()
        value_hbox.addWidget(value_label)
        value_hbox.addWidget(self.value_edit)

        # Unit
        unit_label = QLabel("Unit:")
        self.unit_combobox = QComboBox()
        unit = ""
        if self.component.units is not None:
            print(self.component.componentUnit)
            unit = self.component.componentUnit
            # self.unit_combobox.setCurrentText(unit)
            self.unit_combobox.addItems(self.component.units)
        self.unit_combobox.setCurrentText(unit)
        unit_hbox = QHBoxLayout()
        unit_hbox.addWidget(unit_label)
        unit_hbox.addWidget(self.unit_combobox)

        # Action Buttons
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.on_save)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.on_cancel)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_item)
        action_hbox = QHBoxLayout()
        action_hbox.addWidget(save_button)
        action_hbox.addWidget(cancel_button)

        # # Add to layout
        # preview_scene = QGraphicsView()
        # scene = QGraphicsScene()
        # preview_item = self.component.symbol
        # preview_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        # preview_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        # scene.addItem(preview_item)
        # preview_scene.setScene(scene)
        # # preview_scene.setSceneRect(10, 10, 240, 100)
        # preview_scene.setMaximumHeight(150)
        # layout.addWidget(preview_scene)
        layout.addLayout(name_hbox)
        if self.component.componentType != "Ground":
            layout.addLayout(value_hbox)
        if self.component.units is not None:
            layout.addLayout(unit_hbox)
        if self.component.componentType == "Diode":
            self.diode_characteristics(layout)
        layout.addLayout(action_hbox)
        layout.addWidget(delete_button)

    def diode_characteristics(self, layout):
        # Is
        attribute1_label = QLabel("Is:")
        self.attribute1 = QLineEdit(self)
        self.attribute1.setText(self.component.Is)
        attribute1_unit = QLabel("nA")
        attribute1_hbox = QHBoxLayout()
        attribute1_hbox.addWidget(attribute1_label)
        attribute1_hbox.addWidget(self.attribute1)
        attribute1_hbox.addWidget(attribute1_unit)

        # Rs
        attribute2_label = QLabel("Rs:")
        self.attribute2 = QLineEdit(self)
        self.attribute2.setText(self.component.Rs)
        attribute2_unit = QLabel("Ohms")
        attribute2_hbox = QHBoxLayout()
        attribute2_hbox.addWidget(attribute2_label)
        attribute2_hbox.addWidget(self.attribute2)
        attribute2_hbox.addWidget(attribute2_unit)

        # BV
        attribute3_label = QLabel("BV:")
        self.attribute3 = QLineEdit(self)
        self.attribute3.setText(self.component.BV)
        attribute3_unit = QLabel("V")
        attribute3_hbox = QHBoxLayout()
        attribute3_hbox.addWidget(attribute3_label)
        attribute3_hbox.addWidget(self.attribute3)
        attribute3_hbox.addWidget(attribute3_unit)

        # IBV
        attribute4_label = QLabel("IBV:")
        self.attribute4 = QLineEdit(self)
        self.attribute4.setText(self.component.IBV)
        attribute4_unit = QLabel("V")
        attribute4_hbox = QHBoxLayout()
        attribute4_hbox.addWidget(attribute4_label)
        attribute4_hbox.addWidget(self.attribute4)
        attribute4_hbox.addWidget(attribute4_unit)

        # N
        attribute5_label = QLabel("N:")
        self.attribute5 = QLineEdit(self)
        self.attribute5.setText(self.component.N)
        attribute5_hbox = QHBoxLayout()
        attribute5_hbox.addWidget(attribute5_label)
        attribute5_hbox.addWidget(self.attribute5)

        layout.addLayout(attribute1_hbox)
        layout.addLayout(attribute2_hbox)
        layout.addLayout(attribute3_hbox)
        layout.addLayout(attribute4_hbox)
        layout.addLayout(attribute5_hbox)

    def wire_data(self, layout):
        # Create a QLabel for the large text
        label = QLabel("Component Type: WIRE", self)

        # Set font properties for the label (large text)
        font = QFont()
        font.setPointSize(9)  # Set the font size to 20 points
        font.setBold(True)  # Set the font weight to bold
        label.setFont(font)

        # Align the label to the top left
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Add the label to the layout
        layout.addWidget(label)

        # Add Component data
        wire_name = QLabel("Wire Name:")
        self.wire_name_edit = QLineEdit(self)
        self.wire_name_edit.setText(self.wire.wireName)
        name_hbox = QHBoxLayout()
        name_hbox.addWidget(wire_name)
        name_hbox.addWidget(self.wire_name_edit)

        # Color
        color_label = QLabel("Color:")
        self.unit_combobox = QComboBox()
        colors = self.wire.colors.keys()
        self.unit_combobox.addItems(colors)
        self.unit_combobox.setCurrentText(self.wire.wireColourText)
        unit_hbox = QHBoxLayout()
        unit_hbox.addWidget(color_label)
        unit_hbox.addWidget(self.unit_combobox)

        # Action Buttons
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.on_wire_save)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.on_wire_cancel)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_wire)
        action_hbox = QHBoxLayout()
        action_hbox.addWidget(save_button)
        action_hbox.addWidget(cancel_button)

        layout.addLayout(name_hbox)
        # layout.addLayout(value_hbox)
        layout.addLayout(unit_hbox)
        layout.addLayout(action_hbox)
        layout.addWidget(delete_button)

    def no_component_selected(self, layout):
        label = QLabel("No component selected", self)

        # Set font properties for the label (large text)
        font = QFont()
        font.setPointSize(8)  # Set the font size to 20 points
        font.setBold(False)  # Set the font weight to bold
        label.setFont(font)

        # Align the label to the top left
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Add the label to the layout
        layout.addWidget(label)

    def update_ui(self):
        # Clear existing layout
        # while layout_item := self.layout.takeAt(0):  # Start from index 1 to skip the label
        #     if widget := layout_item.widget():
        #         widget.deleteLater()

        self.clear_layout()

        if self.component is None:
            self.component_data_label.setText("No component selected")

        self.init_ui()

    def clear_layout(self, layout=None):
        if layout is None:
            layout = self.layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                layout.removeWidget(widget)
                widget.deleteLater()
            else:
                sub_layout = item.layout()
                if layout is not None:
                    self.clear_layout(sub_layout)

    def on_canvas_component_select(self, component):
        self.component = component
        # print("connected attribPane")
        # print(self.component.componentID)

        # update the attribute pane
        self.update_ui()

    def on_canvas_component_deselect(self):
        self.component = None
        # print("connected attribPane")
        # print(self.component.componentID)

        # update the attribute pane
        self.update_ui()

    def on_canvas_wire_select(self, component):
        self.wire = component
        # print("connected attribPane")
        # print(self.component.componentID)

        # update the attribute pane
        self.update_ui()

    def on_canvas_wire_deselect(self):
        self.wire = None
        # print("connected attribPane")
        # print(self.component.componentID)

        # update the attribute pane
        self.update_ui()

    def on_save(self):
        self.component.componentName = self.wire_name_edit.text()
        self.component.componentValue = self.value_edit.text()
        unit = self.unit_combobox.currentText()
        self.component.set_unit(unit)
        self.component.symbol.set_name(self.wire_name_edit.text())
        self.component.symbol.set_value(self.value_edit.text())
        self.component.symbol.set_unit(unit)
        if self.component.componentType == "Diode":
            self.component.Is = self.attribute1.text()
            self.component.Rs = self.attribute2.text()
            self.component.BV = self.attribute3.text()
            self.component.IBV = self.attribute4.text()
            self.component.N = self.attribute5.text()
        self.component.symbol.update()
        # print(self.component.componentName)

    def on_cancel(self):
        self.wire_name_edit.setText(self.component.componentName)
        self.value_edit.setText(self.component.componentValue)
        if self.component.componentType == "Diode":
            self.attribute1.setText(self.component.Is)
            self.attribute2.setText(self.component.Rs)
            self.attribute3.setText(self.component.BV)
            self.attribute4.setText(self.component.IBV)
            self.attribute5.setText(self.component.N)

    def on_delete(self):
        self.signals.deleteComponent.emit(self.component.componentID)
        self.component = None
        self.update_ui()

    def on_wire_save(self):
        self.wire.wireName = self.wire_name_edit.text()
        text = self.unit_combobox.currentText()
        color = self.wire.colors.get(self.unit_combobox.currentText())
        self.wire.set_color(text, color)
        print(self.wire.wireColour)
        self.wire.redraw()

    def on_wire_cancel(self):
        self.wire_name_edit.setText(self.wire.wireName)
        self.unit_combobox.setCurrentText(self.wire.wireColourText)
        # self.value_edit.setText(self.component.componentValue)

    def on_wire_delete(self):
        self.signals.deleteWire.emit(self.wire.wireID)
        self.wire = None
        self.update_ui()

    @staticmethod
    def handle_signal(value):
        print(f"Received signal with value: {value}")
