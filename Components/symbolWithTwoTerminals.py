import typing
from enum import Enum

from PyQt6.QtCore import pyqtSignal, QPointF, QRectF, QPoint, Qt
from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtWidgets import QGraphicsObject, QWidget, QGraphicsItem


class Terminal(Enum):
    none = None
    terminal1 = 1
    terminal2 = 2


class SymbolWithTwoTerminals(QGraphicsItem):
    class Signals(QGraphicsObject):
        # signal sends (uniqueID, terminalIndex) as arguments.
        terminalClicked = pyqtSignal(QPointF, int)
        componentMoved = pyqtSignal()
        componentSelected = pyqtSignal()
        componentDeselected = pyqtSignal(str)
        componentDataChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.width = 90
        self.height = 70
        self.terminalLength = 5
        self.padding = 10

        # enum for terminal
        self.terminalCLicked = Terminal.none

        # make symbol selectable and movable
        self.selected = False

        # item is selectable
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        # item can be dragged
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        # item can be highlighted
        self.hoveredTerminal = None
        self.setAcceptHoverEvents(True)
        self.brush = QBrush()
        self.brush.setColor(Qt.GlobalColor.darkRed)

        # set signals
        self.signals = self.Signals()

        painter = QPainter()
        pen = QPen()

    def paint(self, painter, option, widget: typing.Optional[QWidget] = ...) -> None:
        # initialize painter
        pen = QPen()
        painter.setPen(pen)
        body_w = self.width - (2 * self.terminalLength)

        # Get the 4 corners of the rectangle in the resistor
        point_a = QPointF(self.terminalLength, 0)
        point_b = QPointF(self.terminalLength + body_w, 0)
        point_c = QPointF(point_b.x(), point_b.y() + self.height)
        point_d = QPointF(point_a.x(), point_a.y() + self.height)

        # Draw the edges of the rectangle in the resistor
        painter.drawLine(point_a, point_b)
        painter.drawLine(point_b, point_c)
        painter.drawLine(point_c, point_d)
        painter.drawLine(point_d, point_a)

        t1_a = QPointF(0, self.height // 2)
        t1_b = QPointF(self.terminalLength, self.height // 2)
        t2_a = QPointF(self.width - self.terminalLength, self.height // 2)
        t2_b = QPointF(self.width, self.height // 2)

        # draw terminals from their endpoints
        painter.drawLine(t1_a, t1_b)
        painter.drawLine(t2_a, t2_b)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # draw connectors on terminals
        if self.terminalCLicked == Terminal.terminal1:
            painter.drawEllipse(self.width, (self.height // 2) - 4, 7, 7)  # terminal 2
            brush = QPen()
            brush.setWidth(3)
            brush.setColor(Qt.GlobalColor.blue)
            painter.setPen(brush)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.drawEllipse(-self.terminalLength - 3, (self.height // 2) - 4, 7, 7)  # terminal 1
        elif self.terminalCLicked == Terminal.terminal2:
            painter.drawEllipse(-self.terminalLength - 3, (self.height // 2) - 4, 7, 7)  # terminal 1
            brush = QPen()
            brush.setWidth(3)
            brush.setColor(Qt.GlobalColor.blue)
            painter.setPen(brush)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.drawEllipse(self.width, (self.height // 2) - 4, 7, 7)  # terminal 2
        else:
            painter.drawEllipse(-self.terminalLength - 3, (self.height // 2) - 4, 7, 7)  # terminal 1
            painter.drawEllipse(self.width, (self.height // 2) - 4, 7, 7)  # terminal 2

        # painter.drawEllipse(-self.terminalLength - 3, (self.height // 2) - 4, 7, 7)  # terminal 1
        # painter.drawEllipse(self.width, (self.height // 2) - 4, 7, 7)  # terminal 2

        # draw selection box
        if self.isSelected():
            painter.setPen(QPen(Qt.GlobalColor.red, 0.3, Qt.PenStyle.DashLine))
            painter.drawRect(self.boundingRect())

    def mousePressEvent(self, event) -> None:
        self.brush.setColor(Qt.GlobalColor.gray)
        if -self.terminalLength - 3 <= event.pos().x() <= -self.terminalLength + 8 \
                and self.height // 2 - 3 <= event.pos().y() <= self.height // 2 + 8:
            self.terminalCLicked = Terminal.terminal1
            # self.signals.terminalClicked.emit(event.pos(), 1)
            self.terminal_click_slot(event.pos(), 1)
        elif self.width - 3 <= event.pos().x() <= self.width + 8 \
                and self.height // 2 - 3 <= event.pos().y() <= self.height // 2 + 8:
            self.terminalCLicked = Terminal.terminal2
            # self.signals.terminalClicked.emit(event.pos(), 2)
            self.terminal_click_slot(event.pos(), 2)
        else:
            self.terminalCLicked = Terminal.none

        self.update()

        # emit selected
        self.component_click_slot()

    def terminal_click_slot(self, terminal_position, terminal_id):
        self.signals.terminalClicked.emit(terminal_position, terminal_id)

    def component_click_slot(self):
        self.signals.componentSelected.emit()

    def hoverLeaveEvent(self, event) -> None:
        self.brush.setColor(Qt.GlobalColor.darkRed)

    def boundingRect(self):
        return QRectF(
            -self.padding,
            -self.padding,
            self.width + (2 * self.padding),
            self.height + (2 * self.padding),
        )
