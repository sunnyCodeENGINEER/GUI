import typing
from typing import List, Tuple

from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QGraphicsView, QGraphicsScene, \
    QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsPathItem, QGraphicsItem, QWidget, QLineEdit, QInputDialog, \
    QMessageBox
from PyQt6.QtGui import QPixmap, QPen, QPainter, QColor, QAction, QPainterPath, QBrush
from PyQt6.QtCore import QSize, Qt, QPoint, QPointF, QObject, pyqtSignal

from Components.CircuitNode.circuitNode import CircuitNode
from Components.Test import SymbolWithTerminalTest
from Components.Wire.wireComponent import WireDrawing, ConnectedLinesGroup, Wire
from Components.symbol import Symbol
from Components.symbolWithThreeTerminals import SymbolWithThreeTerminals
from Components.symbolWithTwoTerminals import SymbolWithTwoTerminals
from Components.symbolWithOneTerminal import SymbolWithOneTerminal
from Components.allTerminalComponent import OneTerminalComponent, ThreeTerminalComponent, TwoTerminalComponent


class MovingObject(QGraphicsRectItem):
    def __init__(self, x, y, r):
        super(MovingObject, self).__init__(0, 0, r, r)
        self.setPos(x, y)
        self.rr = r
        self.setBrush(Qt.GlobalColor.blue)
        self.setAcceptHoverEvents(True)

        # self.width = 70
        # self.height = 70
        # self.terminalLength = 5
        self.padding = 7

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem',
              widget: typing.Optional[QWidget] = ...) -> None:
        pen = QPen()
        painter.setPen(pen)
        brush = QBrush()
        painter.setBrush(self.brush())

        painter.drawEllipse(0, 0, self.rr, self.rr)

    # make changes to symbol when hovered on
    def hoverEnterEvent(self, event) -> None:
        self.setBrush(Qt.GlobalColor.green)
        print("hoe-ver")

    def hoverLeaveEvent(self, event) -> None:
        self.setBrush(Qt.GlobalColor.blue)

    # move symbol when dragged
    def mousePressEvent(self, event) -> None:
        pass

    def mouseMoveEvent(self, event) -> None:
        original_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        original_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - original_cursor_position.x() + original_position.x()
        updated_cursor_y = updated_cursor_position.y() - original_cursor_position.y() + original_position.y()

        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event) -> None:
        print(event.pos().x(), event.pos().y())


class CustomPathItem(QGraphicsPathItem):
    # possible wire implementation
    def __init__(self, path=None, parent=None):
        super().__init__(parent)
        self.setAcceptHoverEvents(True)
        self.setBrush(Qt.GlobalColor.blue)
        self.pen().setWidth(10)
        self.pen = QPen()
        # self.pen.setWidth(50)
        # self.setFlag(QGraphicsItem.ItemIsSelectable)
        # self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable)

        if path is None:
            self.path = QPainterPath()
        else:
            self.path = path

    def paint(self, painter, option, widget: typing.Optional[QWidget] = ...) -> None:

        painter.setPen(self.pen)
        # painter.setBrush(self.brush())
        painter.drawPath(self.path)

    def boundingRect(self):
        return self.path.boundingRect()

    def hoverEnterEvent(self, event) -> None:
        self.pen.setWidth(20)

    def hoverLeaveEvent(self, event) -> None:
        self.pen.setWidth(50)

    # move symbol when dragged
    def mousePressEvent(self, event) -> None:
        pass

    def mouseMoveEvent(self, event) -> None:
        original_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        original_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - original_cursor_position.x() + original_position.x()
        updated_cursor_y = updated_cursor_position.y() - original_cursor_position.y() + original_position.y()

        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event) -> None:
        print(event.pos().x(), event.pos().y())


class MyGraphicsView(QGraphicsView):
    class Signals(QObject):
        componentSelected = pyqtSignal(OneTerminalComponent)
        componentDeselected = pyqtSignal()
        wireSelected = pyqtSignal(Wire)
        wireDeselected = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.canvas = QPixmap(QSize(400, 400))
        self.label = QLabel()
        self.size = 2

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 1200, 1000)

        # keep track of components on the canvas
        self.canvasComponents = {}
        # keep track of wires on the canvas
        self.wires = {}
        self.currentWire = None
        self.clickedTerminals: List[Tuple] = []
        self.wireToolActive = False
        self.selectedComponent = None

        # keep track of wire start and end points
        self.wirePoints = []
        self.terminalPoint = []
        self.terminalPointIndex = 0

        # will all go!
        self.moveObject = MovingObject(50, 50, 40)
        # self.moveObject2 = MovingObject(10, 50, 30)

        self.moveObject3 = SymbolWithTwoTerminals("name")
        self.moveObject2 = SymbolWithThreeTerminals("name")
        # self.moveObject4 = TwoTerminalComponent("Transistor001", "Transistor-1")
        points = [QPoint(20, 20), QPoint(20, 80), QPoint(20, 100)]
        self.nodeTest1 = WireDrawing(points)

        # self.scene.addItem(self.moveObject4.symbol)

        # self.scene.addItem(self.nodeTest1)

        self.signals = self.Signals()

        # OneTerminalComponent.Signals.componentSelected.connect(self.handle_signal)

    def _connect_signals(self, component):

        component.signals.terminalClicked.connect(self.terminal_clicked)  # will be uncommented when working on wire
        component.signals.componentSelected.connect(self.component_selected)
        component.signals.componentDeselected.connect(self.component_deselected)

    def _connect_wire_signals(self, wire):
        wire.signal.wireSelected.connect(self.wire_selected)
        wire.signal.wireDeselected.connect(self.wire_deselected)

    def component_selected(self, component_id):
        # emit component with the selected id to attribute pane
        self.signals.componentSelected.emit(self.canvasComponents.get(component_id))
        self.selectedComponent = self.canvasComponents.get(component_id)

        for item in self.wires:
            print(item)

    def component_deselected(self):
        # emit component with the selected id to attribute pane
        self.signals.componentDeselected.emit()

        self.selectedComponent = None

    def wire_selected(self, wire_id):
        # emit component with the selected id to attribute pane
        self.signals.wireSelected.emit(self.wires.get(wire_id))
        print("Thesis Maame")
        # self.selectedComponent = self.canvasComponents.get(component_id)

    def wire_deselected(self):
        # emit component with the selected id to attribute pane
        self.signals.wireDeselected.emit()

        # self.selectedComponent = None

    def terminal_clicked(self, component_id, point, terminal_id):
        # check if wire tool is active
        if self.wireToolActive:
            # append component ID and Terminal ID to clickedTerminals
            terminal_tuple = (component_id, terminal_id)
            self.clickedTerminals.append(terminal_tuple)
            print(self.clickedTerminals)
            self.terminalPoint.append(point)
            print(self.terminalPoint)

            # if clickedTerminals count = 2
            if len(self.clickedTerminals) == 2:
                self.wirePoints = []
                # bring pop up for wire name and set up wire
                self.currentWire = Wire()
                unique_count = self.generate_unique_wire_count()
                # self.currentWire.wireID = f"wire-{len(self.wires) + 1}"
                self.currentWire.wireID = f"wire-{unique_count}"
                print(self.currentWire.wireID)
                self.currentWire.wireName = self.show_input_dialog()
                if self.currentWire.wireName is None:
                    pass
                print(self.currentWire.wireName)

                # if one component is a Ground change wire ID to ground
                for item in self.clickedTerminals:
                    component_id = item[0]
                    if component_id.startswith("Ground"):
                        self.currentWire.wireID = "ground"

                # # add wire to self.wires
                # self.wires[wire.wireID] = wire

                try:
                    self._connect_wire_signals(self.currentWire)
                    print("wire signals connected successfully")
                except Exception as e:
                    print(f"There was a problem connecting the signals: {e}")

                # loop over clickedTerminals set corresponding terminal to wire ID
                for index, item in enumerate(self.clickedTerminals):
                    # self.terminalPointIndex += 1
                    component_id, terminal_id = item
                    # add component ID to componentsConnected attribute for wire
                    connected_component_tuple = component_id, terminal_id
                    self.currentWire.connectedComponents.append(connected_component_tuple)
                    print(f"\n\nComponents connected are: {self.currentWire.connectedComponents}")
                    component = self.canvasComponents.get(component_id)
                    self.wirePoints.append(component.symbol.scenePos() + self.terminalPoint[index])
                    self.terminalPointIndex += 1
                    if terminal_id == 1:
                        component.terminal1to = self.currentWire.wireID
                        # print(component.terminal1to)
                    elif terminal_id == 2:
                        component.terminal2to = self.currentWire.wireID
                        # print(component.terminal2to)
                    elif terminal_id == 3:
                        component.terminal3to = self.currentWire.wireID
                        # print(component.terminal3to)
                    # reset component terminal selected to none
                    component.reset_terminal()

                # clear self.clickedTerminals
                self.clickedTerminals.clear()
                self.currentWire.uiWire = WireDrawing(self.wirePoints)
                # add wire to self.wires
                self.wires[self.currentWire.wireID] = self.currentWire
                print(self.wires)

                self.scene.addItem(self.currentWire.uiWire)
                # self.draw_wire()
                self.terminalPoint = []

    def draw_wire(self):
        self.nodeTest1 = WireDrawing(self.wirePoints)
        self.scene.addItem(self.nodeTest1)
        # self.wirePoints.clear()

    def show_input_dialog(self):
        # Create an input dialog
        text, ok_pressed = QInputDialog.getText(self, 'Name Wire', 'Enter Wire name:')

        # Check if OK button is pressed and handle the input
        if ok_pressed and text.strip():
            QMessageBox.information(self, 'Message', f'Wire {text} added.')
            # name = text
            return text
        else:
            return None

    def rotate_selected_components(self):
        # for componentID in self.selectedComponentsIDs:
        #     component = self.components.get(componentID)
        #     component.rotate()
        if self.selectedComponent is None:
            pass

        self.selectedComponent.symbol.rotate()

    def generate_component(self, component_type):
        pass

    def add_component(self, component):
        # generate the unique count for the component
        unique_count = self.generate_unique_component_count(component.componentName)
        print(f"Unique count for {component.componentType} : {unique_count}")
        # set ID and name
        component.componentID = f"{component.componentType}-{unique_count}"
        component.componentName = f"{component.componentType}-{unique_count}"
        component.symbol.set_name(f"{component.componentType}-{unique_count}")
        print(f"{component.componentID} : {component.componentName} : {component.componentType}")
        # add component and its ID to dictionary
        self.canvasComponents[component.componentID] = component
        try:
            self._connect_signals(component)
            print("signals connected successfully")
        except Exception as e:
            print(f"There was a problem connecting the signals: {e}")
        print(self.canvasComponents.keys())
        self.scene.addItem(component.symbol)

    def delete_component(self, component_id):
        print("\n\n\n")
        print("-----------------------------------------------")
        print(component_id)
        wires = []
        for item in self.wires:
            print(item)
            wires.append(self.wires.get(item))
        print(self.wires)
        print(wires)

        # loop over self.wires and remove wires with component ID from the scene
        wire_ids_to_delete = []
        # [item for item in wires if item.connectedComponents[0] == component_id]
        for item in wires:
            print(item.connectedComponents)
            for obj in item.connectedComponents:
                print(f"obj {obj}")
                if obj[0] == component_id:
                    wire_ids_to_delete.append(item.wireID)
        print(f"wire ids to delete: {wire_ids_to_delete}")
        wires_to_delete = []
        for item in wire_ids_to_delete:
            print(f"item: {item}")
            wires_to_delete.append(self.wires.get(item))
        print(wires_to_delete)
        for wire in wires_to_delete:
            print("its about to go down")
            self.scene.removeItem(wire.uiWire)
            for component in wire.connectedComponents:
                #     # clear all necessary components that have their terminal'X'to attribute pointing to the wire
                print(component)
                actual_component = self.canvasComponents.get(component[0])
                if component[1] == 1:
                    print("makes sense")
                    actual_component.terminal1to = ""
                    #         component[0].set_terminal_1_to("")
                elif component[1] == 2:
                    print("makes sense")
                    try:
                        actual_component.terminal2to = ""
            #         component[0].set_terminal_2_to("")
                    except Exception as e:
                        print(e)
                elif component[1] == 3:
                    print("makes sense")
                    actual_component.terminal31to = ""
            #         component[0].set_terminal_3_to("")
        # loop over self.wires and remove wires with component ID from self.wires
        # filtered_wires = [item for item in self.wires if item[0] != component_id]
        # self.wires = filtered_wires
        for wire_id in wire_ids_to_delete:
            _ = self.wires.pop(wire_id)
        print(f"self.wires: {self.wires}")

        component = self.canvasComponents.get(component_id)
        # remove components symbol from canvas
        try:
            self.scene.removeItem(component.symbol)
        except Exception as e:
            print(f"there was an error removing symbol from scene: {e}")
        # remove component from dictionary
        _ = self.canvasComponents.pop(component_id)  # will be used when working on undo and redo
        print(self.canvasComponents.keys())

    def generate_unique_wire_count(self) -> int:
        # get all the wireIDs available
        existing_ids = self.wires.keys()
        print(f"existing_ids : {existing_ids}")
        # # filter the IDs to get only the ones that start with the component name
        # print(f"component_name: {component_name}")
        filtered_ids = list(filter(lambda x: x.startswith("wire"), existing_ids))
        # print(f"filtered_ids: {filtered_ids}")
        # if there are no existing IDs, return 0
        # filtered_ids = existing_ids
        if len(filtered_ids) == 0:
            return 1
        # sort the IDs in ascending order
        filtered_ids.sort()
        # get the last ID
        last_id = filtered_ids[-1]
        # get the unique count from the last ID
        unique_count = int(last_id.split("-")[-1])
        print(f"unique_count: {unique_count}")
        # increment the unique count by 1
        unique_count += 1
        return unique_count

    def generate_unique_component_count(self, component_name: str) -> int:
        """
        Function to generate the unique component count for a component name.

        Params:
            component_name: `str` the name of the component to generate the unique count for

        Returns:
            `int` the unique count for the component name
        """
        # get all the componentIDs available
        existing_ids = self.canvasComponents.keys()
        print(f"existing_ids : {existing_ids}")
        # filter the IDs to get only the ones that start with the component name
        print(f"component_name: {component_name}")
        filtered_ids = list(filter(lambda x: x.startswith(component_name), existing_ids))
        print(f"filtered_ids: {filtered_ids}")
        # if there are no existing IDs, return 0
        if len(filtered_ids) == 0:
            return 1
        # sort the IDs in ascending order
        filtered_ids.sort()
        # get the last ID
        last_id = filtered_ids[-1]
        # get the unique count from the last ID
        unique_count = int(last_id.split("-")[-1])
        print(f"unique_count: {unique_count}")
        # increment the unique count by 1
        unique_count += 1
        return unique_count

    def on_wire_tool_click(self, wire_tool_state: bool):
        self.wireToolActive = wire_tool_state

    @staticmethod
    def handle_signal(value):
        print(f"Received signal with value: {value}")


class InputDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.lineEdit = QLineEdit()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Input Dialog Example')

        layout = QVBoxLayout()

        # Create a line edit widget for input
        # self.lineEdit = QLineEdit(self)
        layout.addWidget(self.lineEdit)

        # Create a button to trigger the input dialog
        button = QPushButton('Get Input', self)
        button.clicked.connect(self.showInputDialog)
        layout.addWidget(button)

        self.setLayout(layout)

    def showInputDialog(self):
        # Create an input dialog
        text, ok_pressed = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')

        # Check if OK button is pressed and handle the input
        if ok_pressed and text.strip():
            QMessageBox.information(self, 'Message', f'Hello, {text}!')

# app = QApplication([])
# window = MyGraphicsView()
# window.show()
# app.exec()
