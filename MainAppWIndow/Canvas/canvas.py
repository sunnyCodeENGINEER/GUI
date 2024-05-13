import typing

from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QGraphicsView, QGraphicsScene, \
    QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsPathItem, QGraphicsItem, QWidget
from PyQt6.QtGui import QPixmap, QPen, QPainter, QColor, QAction, QPainterPath, QBrush
from PyQt6.QtCore import QSize, Qt, QPoint, QPointF, QObject, pyqtSignal

from Components.CircuitNode.circuitNode import CircuitNode
from Components.Test import SymbolWithTerminalTest
from Components.Wire.wireComponent import WireDrawing, ConnectedLinesGroup
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

        # will all go!
        self.moveObject = MovingObject(50, 50, 40)
        # self.moveObject2 = MovingObject(10, 50, 30)

        self.moveObject3 = SymbolWithTwoTerminals("name")
        self.moveObject2 = SymbolWithThreeTerminals("name")
        # self.moveObject4 = TwoTerminalComponent("Transistor001", "Transistor-1")
        self.nodeTest1 = CircuitNode(0, 0, 10)

        # self.scene.addItem(self.moveObject4.symbol)

        # self.scene.addItem(self.nodeTest1)

        self.signals = self.Signals()

        # OneTerminalComponent.Signals.componentSelected.connect(self.handle_signal)

    def _connect_signals(self, component):

        # component.signals.terminalClicked.connect()  #  will be uncommented when working on wire
        component.signals.componentSelected.connect(self.component_selected)

    def component_selected(self, component_id):
        # emit component with the selected id to attribute pane
        self.signals.componentSelected.emit(self.canvasComponents.get(component_id))

    def generate_component(self, component_type):
        pass

    def add_component(self, component):
        print("arrived here")
        print(component.componentName)
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
        component = self.canvasComponents.get(component_id)
        # remove components symbol from canvas
        try:
            self.scene.removeItem(component.symbol)
        except Exception as e:
            print(f"there was an error removing symbol from scene: {e}")
        # remove component from dictionary
        _ = self.canvasComponents.pop(component_id)  # will be used when working on undo and redo
        print(self.canvasComponents.keys())

    def generate_unique_component_count(self, component_name: str) -> int:
        """
        Function to generate the unique component count for a component name.

        Params:
            component_name: `str` the name of the component to generate the unique count for

        Returns:
            `int` the unique count for the component name
        """
        print("working")
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

    @staticmethod
    def handle_signal(value):
        print(f"Received signal with value: {value}")

# app = QApplication([])
# window = MyGraphicsView()
# window.show()
# app.exec()
