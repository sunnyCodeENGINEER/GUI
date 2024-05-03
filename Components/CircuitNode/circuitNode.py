import typing

from PyQt6 import QtGui
from PyQt6.QtCore import pyqtSignal, QPointF, QRectF, QPoint, Qt
from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtWidgets import QGraphicsObject, QWidget, QGraphicsItem, QGraphicsRectItem


class CircuitNode(QGraphicsRectItem):

    class Signals(QGraphicsObject):
        # signal sends (uniqueID, terminalIndex) as arguments.
        nodeClicked = pyqtSignal(str, int)
        nodeMoved = pyqtSignal()
        nodeSelected = pyqtSignal(str)
        nodeDeselected = pyqtSignal(str)
        nodeDataChanged = pyqtSignal()

    def __init__(self, x, y, r):
        super().__init__(0, 0, r, r)
        self.setPos(x, y)
        self.rr = r
        self.setBrush(Qt.GlobalColor.blue)
        self.setAcceptHoverEvents(True)
        self.selected = False

        self.padding = 7

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem',
              widget: typing.Optional[QWidget] = ...) -> None:
        pen = QPen()
        painter.setPen(pen)
        brush = QBrush()
        painter.setBrush(self.brush())

        painter.drawEllipse(0, 0, self.rr, self.rr)

        if self.selected:
            self.setBrush(Qt.GlobalColor.red)

    # make changes to symbol when hovered on
    def hoverEnterEvent(self, event) -> None:
        self.setBrush(Qt.GlobalColor.green)
        print("hoe-ver")

    def hoverLeaveEvent(self, event) -> None:
        self.setBrush(Qt.GlobalColor.blue)

    # move symbol when dragged
    def mousePressEvent(self, event) -> None:
        self.selected = not self.selected
        print(self.selected)

    def mouseMoveEvent(self, event) -> None:
        original_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        original_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - original_cursor_position.x() + original_position.x()
        updated_cursor_y = updated_cursor_position.y() - original_cursor_position.y() + original_position.y()

        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event) -> None:
        print(event.pos().x(), event.pos().y())
