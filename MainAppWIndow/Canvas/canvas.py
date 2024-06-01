import typing
from array import array
from typing import List, Tuple

import numpy
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QGraphicsView, QGraphicsScene, \
    QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsPathItem, QGraphicsItem, QWidget, QLineEdit, QInputDialog, \
    QMessageBox, QDialogButtonBox, QComboBox, QDialog
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
from MainAppWIndow.Canvas.CanvasGrid.grid_scene import GridScene
from Middleware.circuitSimulationMiddleware import SimulationMiddleware, ResultPlot


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
        simulate = pyqtSignal()
        simulationData = pyqtSignal(str)
        simulationResult = pyqtSignal(ResultPlot)

    def __init__(self):
        super().__init__()
        self.canvas = QPixmap(QSize(400, 400))
        self.label = QLabel()
        self.size = 2

        # self.scene = QGraphicsScene()
        self.scene = GridScene()
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 1200, 1000)

        self.setOptimizationFlag(
            QGraphicsView.OptimizationFlag.DontAdjustForAntialiasing, True
        )
        # RubberBandDrag mode allows the selection of multiple components by dragging to draw a rectangle around them
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.circuitName: str = ""
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

        self.point1 = None
        self.point2 = None

        points = [QPoint(20, 20), QPoint(20, 80), QPoint(20, 100)]
        self.nodeTest1 = WireDrawing(points)

        self.analysisType = "Operating Point"

        self.circuit = SimulationMiddleware(self.circuitName, self.canvasComponents, self.wires, self.analysisType,
                                                25, 25)
        self.isSimulating = False
        self.simulationResult = None
        self.signals = self.Signals()
        self.signals.simulate.connect(self.simulate)
        self.circuit.signals.simulationData.connect(self.data_received)
        # self.circuit.signals.simulationResult.connect(self.result_received)

    def simulate(self):
        if self.isSimulating:

            # if self.circuitName == "":
            # self.circuitName = self.show_input_dialog(title='Circuit Name', text='Give a name for the circuit:')
            self.circuitName, self.analysisType = self.show_custom_input_dialog(title='Circuit Name',
                                                                                text='Give a name for the circuit:')
            self.circuit = SimulationMiddleware(self.circuitName, self.canvasComponents, self.wires, self.analysisType,
                                                25, 25)
            if self.analysisType == "Transient":
                try:
                    self.simulationResult = self.circuit.run_analysis()
                    self.result_received()
                except Exception as e:
                    print(e)
            self.circuit.signals.simulationResult.connect(self.result_received)
            self.signals.simulationData.emit(f"Circuit Created: {self.circuitName}")
            self.signals.simulationData.emit("======================")
            # try:
            #     self.circuit.signals.simulationData.connect(self.data_received)
            #     self.circuit.signals.simulationResult.connect(self.result_received)
            # except Exception as e:
            #     print(e)

    def result_received(self):
        print("results received")
        print(self.simulationResult.x_axis)
        self.signals.simulationResult.emit(self.simulationResult)

    def data_received(self, text):
        self.signals.simulationData.emit(text)

    def on_simulate(self, state: bool):
        self.isSimulating = state
        self.signals.simulate.emit()

    def _connect_signals(self, component):

        component.signals.terminalClicked.connect(self.terminal_clicked)  # will be uncommented when working on wire
        component.signals.componentSelected.connect(self.component_selected)
        component.signals.componentDeselected.connect(self.component_deselected)
        component.signals.componentMoved.connect(self.component_moved)

    def _connect_wire_signals(self, wire):
        wire.signals.wireSelected.connect(self.wire_selected)
        wire.signals.wireDeselected.connect(self.wire_deselected)
        wire.signals.wirePoint.connect(self.wire_connection_point)

        try:
            for wire_id in wire.connectedTo:
                origin_wire = self.wires.get(wire_id)
                origin_wire.signals.wireMoved.connect(self.wire_moved)

        except Exception as e:
            print(e)

    def redraw_wire_on_origin_move(self, wire, og_wire: Wire, offset):
        i = 0
        for index, point in enumerate(wire.points):
            if point.x() == (og_wire.points[0].x() + og_wire.points[1].x()) / 2 and \
                    point.y() == (og_wire.points[0].y() + og_wire.points[1].y()) / 2:
                i = index
        wire.points[i] += offset
        wire.update()
        self.scene.update()

    def wire_moved(self, unique_id, offset):
        og_wire = self.wires.get(unique_id)
        print(og_wire)
        for wire_id in self.wires:
            wire = self.wires.get(wire_id)
            for _id in wire.connectedTo:
                print(_id)
                if _id == og_wire.wireID:
                    self.redraw_wire_on_origin_move(wire, og_wire, offset)

    def component_moved(self, offset):
        try:
            self.redraw_wire_on_wire_move(offset)
        except Exception as e:
            print(e)
        self.scene.update()

    def component_selected(self, component_id):
        # emit component with the selected id to attribute pane
        self.signals.componentSelected.emit(self.canvasComponents.get(component_id))
        self.selectedComponent = self.canvasComponents.get(component_id)

    def component_deselected(self):
        # emit component with the selected id to attribute pane
        self.signals.componentDeselected.emit()

        self.selectedComponent = None

    def mousePressEvent(self, event: typing.Optional[QtGui.QMouseEvent]) -> None:
        super(MyGraphicsView, self).mousePressEvent(event)
        if self.wireToolActive:
            self.point1 = self.point2
            self.point2 = QPointF(event.pos())

    def on_wire_draw_cancel(self):
        self.clickedTerminals.clear()
        self.terminalPoint.clear()
        return

    def wire_connection_point(self, wire_id):
        if self.wireToolActive:
            if self.clickedTerminals:
                component_id, terminal_id = self.clickedTerminals[-1]
                component = self.canvasComponents.get(component_id)
                origin_wire = self.wires.get(wire_id)
                points = [self.terminalPoint[-1] + component.symbol.scenePos(),
                          QPointF((origin_wire.points[0].x() + origin_wire.points[1].x()) / 2,
                                  (origin_wire.points[0].y() + origin_wire.points[1].y()) / 2)
                          ]
                self.currentWire = Wire(Qt.GlobalColor.darkGreen, "darkGreen", points=points)
                self.currentWire.wireName = self.show_input_dialog()
                if self.currentWire.wireName == "":
                    self.clickedTerminals.clear()
                    self.terminalPoint.clear()
                    self.currentWire = None
                    return
                unique_count = self.generate_unique_wire_count()
                self.currentWire.wireID = f"wire-{unique_count}"
                self.currentWire.connectedTo.append(wire_id)

                # set component's connected to data
                if terminal_id == 1:
                    component.terminal1To = self.currentWire.wireID
                elif terminal_id == 2:
                    component.terminal2To = self.currentWire.wireID
                elif terminal_id == 3:
                    component.terminal3To = self.currentWire.wireID
                # reset component terminal selected to none
                component.reset_terminal()
                self.canvasComponents[component_id] = component

                # self.currentWire = wire
                self._connect_wire_signals(self.currentWire)

                try:
                    self.wires[self.currentWire.wireID] = self.currentWire
                except Exception as e:
                    print(e)
                try:
                    self.scene.addItem(self.currentWire)
                    print(self.wires)
                    # clear points
                    self.point1 = None
                    self.point2 = None
                    self.clickedTerminals.clear()
                    return
                except Exception as e:
                    print(e)

                pass
            elif self.point2 is not None and self.point1 is not None:
                origin_wire = self.wires.get(wire_id)
                points = [QPointF((origin_wire.points[0].x() + origin_wire.points[1].x()) / 2,
                                  (origin_wire.points[0].y() + origin_wire.points[1].y()) / 2),
                          self.point2
                          ]

                self.currentWire = Wire(Qt.GlobalColor.darkGreen, "darkGreen", points=points)
                self.currentWire.wireName = self.show_input_dialog()
                if self.currentWire.wireName == "":
                    self.clickedTerminals.clear()
                    self.terminalPoint.clear()
                    return
                unique_count = self.generate_unique_wire_count()
                self.currentWire.wireID = f"wire-{unique_count}"
                self.currentWire.connectedTo.append(wire_id)

                self._connect_wire_signals(self.currentWire)
                try:
                    self.wires[self.currentWire.wireID] = self.currentWire
                except Exception as e:
                    print(e)
                try:
                    self.scene.addItem(self.currentWire)
                    print(self.wires)
                    # clear points
                    self.point1 = None
                    self.point2 = None
                    return
                except Exception as e:
                    print(e)

                # self.points = []
        #         pass

    def wire_selected(self, wire_id):
        # emit component with the selected id to attribute pane
        self.signals.wireSelected.emit(self.wires.get(wire_id))
        if self.isSimulating:
            _ = self.wires.get(wire_id)
            wire_name = _.wireName
            self.circuit.set_node(wire_id, wire_name)
            self.circuit.run_analysis()
        # print("Thesis Maame")
        # self.selectedComponent = self.canvasComponents.get(component_id)

    def wire_deselected(self):
        # emit component with the selected id to attribute pane
        self.signals.wireDeselected.emit()
        # print("Thesis Papa")

        # self.selectedComponent = None

    def terminal_clicked(self, component_id, point, terminal_id):
        # check if wire tool is active
        if self.wireToolActive:
            # append component ID and Terminal ID to clickedTerminals
            terminal_tuple = (component_id, terminal_id)
            self.clickedTerminals.append(terminal_tuple)
            self.terminalPoint.append(point)

            if len(self.clickedTerminals) == 2:
                self.wirePoints = []
                # bring pop up for wire name and set up wire
                self.currentWire = Wire(Qt.GlobalColor.darkGreen, "darkGreen")
                unique_count = self.generate_unique_wire_count()
                self.currentWire.wireID = f"wire-{unique_count}"
                self.currentWire.wireName = self.show_input_dialog()
                if self.currentWire.wireName == "":
                    self.clickedTerminals.clear()
                    self.terminalPoint.clear()
                    return
                if self.currentWire.wireName is None:
                    return

                # if one component is a Ground change wire ID to ground
                for item in self.clickedTerminals:
                    component_id = item[0]
                    if component_id.startswith("Ground"):
                        unique_count = self.generate_unique_ground_wire_count()
                        self.currentWire.wireID = f"ground-{unique_count}"

                try:
                    self._connect_wire_signals(self.currentWire)
                except Exception as e:
                    print(f"There was a problem connecting the signals: {e}")

                # loop over clickedTerminals set corresponding terminal to wire ID
                for index, item in enumerate(self.clickedTerminals):
                    # self.terminalPointIndex += 1
                    component_id, terminal_id = item
                    # add component ID to componentsConnected attribute for wire
                    connected_component_tuple = component_id, terminal_id
                    self.currentWire.connectedComponents.append(connected_component_tuple)
                    component = self.canvasComponents.get(component_id)
                    self.wirePoints.append(component.symbol.scenePos() + self.terminalPoint[index])
                    self.terminalPointIndex += 1
                    if terminal_id == 1:
                        component.terminal1To = self.currentWire.wireID
                    elif terminal_id == 2:
                        component.terminal2To = self.currentWire.wireID
                    elif terminal_id == 3:
                        component.terminal3To = self.currentWire.wireID
                    # reset component terminal selected to none
                    component.reset_terminal()
                    self.canvasComponents[component_id] = component

                # clear self.clickedTerminals
                self.clickedTerminals.clear()
                self.currentWire.uiWire = WireDrawing(self.wirePoints)
                self.currentWire.points = self.wirePoints
                # add wire to self.wires
                self.wires[self.currentWire.wireID] = self.currentWire

                # self.scene.addItem(self.currentWire.uiWire)
                self.scene.addItem(self.currentWire)
                self.point1 = None
                self.point2 = None
                # self.draw_wire()
                self.terminalPoint = []

    def draw_wire(self):
        self.nodeTest1 = WireDrawing(self.wirePoints)
        self.scene.addItem(self.nodeTest1)
        # self.wirePoints.clear()

    def show_custom_input_dialog(self, title='Name Wire', text='Enter Wire name:'):
        options = ["Operating Point", "DC Sweep", "Transient", "AC Analysis"]
        dialog = CustomInputDialog(title, text, options, self)
        wire_name, combo_value = dialog.getInputs()

        if wire_name and combo_value:

            QMessageBox.information(self, 'Message', f'Wire {wire_name} added with {combo_value}.')
            return wire_name, combo_value
        else:
            return None, None

    def show_input_dialog_circuit(self, title='Name Wire', text='Enter Wire name:'):
        # Create an input dialog
        text, ok_pressed = QInputDialog.getText(self, title, text)

        # Check if OK button is pressed and handle the input
        if ok_pressed and text.strip():
            QMessageBox.information(self, 'Message', f'Circuit {text} named.')
            # name = text
            return text
        else:
            return None

    def show_input_dialog(self, title='Name Wire', text='Enter Wire name:'):
        # Create an input dialog
        text, ok_pressed = QInputDialog.getText(self, title, text)

        # Check if OK button is pressed and handle the input
        if ok_pressed and text.strip():
            QMessageBox.information(self, 'Message', f'Wire {text} added.')
            # name = text
            return text
        else:
            return None

    def redraw_wire_on_wire_move(self, offset):
        self.point1 = None
        self.point2 = None
        # return
        wires_to_redraw = []
        try:
            wire_id = self.selectedComponent.terminal1To
            print(wire_id)
            wire = self.wires.get(wire_id)
            print(wire)
            # component specific offset
            comp_offset = QPointF()
            if self.selectedComponent.componentType == "Ground":
                comp_offset = QPointF(-14, -28.0)
            else:
                comp_offset = QPointF(-45, 0)
            # store points
            points = []
            for point in wire.points:
                if point.x() - 30 <= self.selectedComponent.symbol.op.x() + \
                        comp_offset.x() <= point.x() + 30 \
                        and point.y() - 30 <= self.selectedComponent.symbol.op.y() + \
                        comp_offset.y() <= point.y() + 30:
                    point += offset
                else:
                    pass
                points.append(point)
            wire.points = points
            wire.update()
            self.scene.update()
        except Exception as e:
            print(f"no terminal: {e}")
        try:
            wire_id = self.selectedComponent.terminal2To
            # wires_to_redraw.append(wire_id)
            wire = self.wires.get(wire_id)
            # component specific offset
            comp_offset = QPointF(60, 10)
            # store points
            points = []
            for point in wire.points:
                if point.x() - 40 <= self.selectedComponent.symbol.op.x() + \
                        comp_offset.x() <= point.x() + 40 \
                        and point.y() - 40 <= self.selectedComponent.symbol.op.y() + \
                        comp_offset.y() <= point.y() + 40:
                    point += offset
                else:
                    pass
                points.append(point)
                print(point)
                print(points)
            wire.points = points
            wire.update()
            self.scene.update()
        except Exception as e:
            print(f"no terminal: {e}")
        try:
            wire_id = self.selectedComponent.terminal3To
            wire = self.wires.get(wire_id)
            # component specific offset
            comp_offset = QPointF(-20, 20)
            # store points
            points = []
            for point in wire.points:
                if point.x() - 40 <= self.selectedComponent.symbol.op.x() + \
                        comp_offset.x() <= point.x() + 40 \
                        and point.y() - 40 <= self.selectedComponent.symbol.op.y() + \
                        comp_offset.y() <= point.y() + 40:
                    # point = self.selectedComponent.symbol.final_position
                    point += offset
                else:
                    pass
                points.append(point)
            wire.points = points
            wire.update()
            self.scene.update()
        except Exception as e:
            print(f"no terminal: {e}")

    def redraw_wire_on_wire_rotation(self):
        # return
        wires_to_redraw = []
        try:
            wire_id = self.selectedComponent.terminal1To
            print(wire_id)
            wire = self.wires.get(wire_id)
            # store points
            points = []
            for point in wire.points:
                if point.x() - 10 <= self.selectedComponent.symbol.old_terminal1_position.x() + \
                        self.selectedComponent.symbol.scenePos().x() <= point.x() + 10 \
                        and point.y() - 10 <= self.selectedComponent.symbol.old_terminal1_position.y() + \
                        self.selectedComponent.symbol.scenePos().y() <= point.y() + 10:
                    point = self.selectedComponent.symbol.new_terminal1_position + \
                            self.selectedComponent.symbol.scenePos()
                else:
                    pass
                points.append(point)
            wire.points = points
            wire.update()
            self.scene.update()
        except Exception as e:
            print(f"no terminal: {e}")
        try:
            wire_id = self.selectedComponent.terminal2To
            wires_to_redraw.append(wire_id)
        except Exception as e:
            print(f"no terminal: {e}")
        try:
            wire_id = self.selectedComponent.terminal3To
            wires_to_redraw.append(wire_id)
        except Exception as e:
            print(f"no terminal: {e}")

    def rotate_selected_components(self):
        if self.selectedComponent is None:
            return

        if self.wireToolActive:
            QMessageBox.information(self, 'Message', f'Can not perform action when wire tool is active.')
            return

        self.selectedComponent.symbol.rotate()
        self.redraw_wire_on_wire_rotation()

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
        wires = []
        for item in self.wires:
            print(item)
            wires.append(self.wires.get(item))

        # loop over self.wires and remove wires with component ID from the scene
        wire_ids_to_delete = []
        # [item for item in wires if item.connectedComponents[0] == component_id]
        for item in wires:
            print(item.connectedComponents)
            for obj in item.connectedComponents:
                print(f"obj {obj}")
                if obj[0] == component_id:
                    wire_ids_to_delete.append(item.wireID)
        wires_to_delete = []
        for item in wire_ids_to_delete:
            print(f"item: {item}")
            wires_to_delete.append(self.wires.get(item))
        for wire in wires_to_delete:
            print("its about to go down")
            self.scene.removeItem(wire)
            for component in wire.connectedComponents:
                # clear all necessary components that have their terminal'X'to attribute pointing to the wire
                actual_component = self.canvasComponents.get(component[0])
                if component[1] == 1:
                    actual_component.terminal1To = ""
                elif component[1] == 2:
                    try:
                        actual_component.terminal2To = ""
                    except Exception as e:
                        print(e)
                elif component[1] == 3:
                    actual_component.terminal3To = ""

        for wire_id in wire_ids_to_delete:
            _ = self.wires.pop(wire_id)

        component = self.canvasComponents.get(component_id)
        # remove components symbol from canvas
        try:
            self.scene.removeItem(component.symbol)
        except Exception as e:
            print(f"there was an error removing symbol from scene: {e}")
        # remove component from dictionary
        _ = self.canvasComponents.pop(component_id)  # will be used when working on undo and redo
        print(self.canvasComponents.keys())

    def delete_wire(self, wire_id):
        wires = []
        for item in self.wires:
            wires.append(self.wires.get(item))

        # loop over self.wires and remove wires with component ID from the scene
        wire_ids_to_delete = self.wires.get(wire_id)
        print(f"wire ids to delete: {wire_ids_to_delete}")
        wires_to_delete = [self.wires.get(wire_id)]
        wire = self.wires.get(wire_id)

        self.scene.removeItem(wire)
        for component in wire.connectedComponents:
            # clear all necessary components that have their terminal'X'to attribute pointing to the wire
            print(component)
            actual_component = self.canvasComponents.get(component[0])
            if component[1] == 1:
                actual_component.terminal1To = ""
            elif component[1] == 2:
                try:
                    actual_component.terminal2To = ""
                except Exception as e:
                    print(e)
            elif component[1] == 3:
                actual_component.terminal3To = ""
        _ = self.wires.pop(wire_id)

    def generate_unique_wire_count(self) -> int:
        # get all the wireIDs available
        existing_ids = self.wires.keys()
        # filter the IDs to get only the ones that start with the component name
        filtered_ids = list(filter(lambda x: x.startswith("wire"), existing_ids))
        if len(filtered_ids) == 0:
            return 1
        # sort the IDs in ascending order
        filtered_ids.sort()
        # get the last ID
        last_id = filtered_ids[-1]
        # get the unique count from the last ID
        unique_count = int(last_id.split("-")[-1])
        # increment the unique count by 1
        unique_count += 1
        return unique_count

    def generate_unique_ground_wire_count(self) -> int:
        # get all the wireIDs available
        existing_ids = self.wires.keys()
        # filter the IDs to get only the ones that start with the component name
        filtered_ids = list(filter(lambda x: x.startswith("ground"), existing_ids))
        if len(filtered_ids) == 0:
            return 1
        # sort the IDs in ascending order
        filtered_ids.sort()
        # get the last ID
        last_id = filtered_ids[-1]
        # get the unique count from the last ID
        unique_count = int(last_id.split("-")[-1])
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
        # filter the IDs to get only the ones that start with the component name
        filtered_ids = list(filter(lambda x: x.startswith(component_name), existing_ids))
        # if there are no existing IDs, return 0
        if len(filtered_ids) == 0:
            return 1
        # sort the IDs in ascending order
        filtered_ids.sort()
        # get the last ID
        last_id = filtered_ids[-1]
        # get the unique count from the last ID
        unique_count = int(last_id.split("-")[-1])
        # increment the unique count by 1
        unique_count += 1
        return unique_count

    def on_wire_tool_click(self, wire_tool_state: bool):
        self.wireToolActive = wire_tool_state
        self.point1 = None
        self.point2 = None

    @staticmethod
    def handle_signal(value):
        print(f"Received signal with value: {value}")


class CustomInputDialog(QDialog):
    def __init__(self, title='Name Wire', text='Enter Wire name:', options=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)

        self.layout = QVBoxLayout()

        # Add label and line edit
        self.label = QLabel(text)
        self.layout.addWidget(self.label)
        self.line_edit = QLineEdit(self)
        self.layout.addWidget(self.line_edit)

        # Add combo box if options are provided
        self.combo_box = None
        if options:
            self.combo_box = QComboBox(self)
            self.combo_box.addItems(options)
            self.layout.addWidget(self.combo_box)

        # Add standard dialog buttons (Ok and Cancel)
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
                                           self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def getInputs(self):
        if self.exec() == QDialog.DialogCode.Accepted:
            text = self.line_edit.text().strip()
            combo_value = self.combo_box.currentText() if self.combo_box else None
            return text, combo_value
        return None, None


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
