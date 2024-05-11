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

        # will all go!
        self.moveObject = MovingObject(50, 50, 40)
        # self.moveObject2 = MovingObject(10, 50, 30)

        self.moveObject3 = SymbolWithTwoTerminals()
        self.moveObject2 = SymbolWithThreeTerminals()
        self.moveObject4 = TwoTerminalComponent("Transistor001", "Transistor-1")
        self.nodeTest1 = CircuitNode(0, 0, 10)

        self.scene.addItem(self.moveObject4.symbol)

        self.scene.addItem(self.nodeTest1)
        self.signals = self.Signals()

    def addComponent(self):
        pass

# app = QApplication([])
# window = MyGraphicsView()
# window.show()
# app.exec()
