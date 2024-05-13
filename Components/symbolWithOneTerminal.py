import typing
from enum import Enum

from PyQt6.QtCore import pyqtSignal, QPointF, QRectF, Qt
from PyQt6.QtGui import QPainter, QPen, QBrush, QFont
from PyQt6.QtWidgets import QGraphicsObject, QWidget, QGraphicsItem


class Terminal(Enum):
    none = None
    terminal1 = 1


class SymbolWithOneTerminal(QGraphicsItem):
    class Signals(QGraphicsObject):
        # signal sends (uniqueID, terminalIndex) as arguments.
        terminalClicked = pyqtSignal(QPointF, int)
        componentMoved = pyqtSignal()
        componentSelected = pyqtSignal()
        componentDeselected = pyqtSignal(str)
        componentDataChanged = pyqtSignal()

    def __init__(self, name):
        super().__init__()
        self.width = 90
        self.height = 70
        self.terminalLength = 5
        self.padding = 10
        self.name = name

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
        body_h = self.height - (2 * self.terminalLength)

        # Get the 4 corners of the rectangle in the resistor
        point_a = QPointF(0, self.terminalLength + 7)
        point_b = QPointF(self.width, self.terminalLength + 7)
        point_c = QPointF(point_b.x(), point_b.y() + body_h)
        point_d = QPointF(point_a.x(), point_a.y() + body_h)

        # Draw the edges of the rectangle in the resistor
        painter.drawLine(point_a, point_b)
        painter.drawLine(point_b, point_c)
        painter.drawLine(point_c, point_d)
        painter.drawLine(point_d, point_a)

        t1_a = QPointF((self.width // 2), 7)
        t1_b = QPointF((self.width // 2), self.terminalLength + 7)

        # draw terminal from its endpoint
        painter.drawLine(t1_a, t1_b)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # draw component name
        font = QFont("Arial", 8)  # Specify font family and font size (e.g., 12 points)
        painter.setFont(font)
        painter.drawText(10, self.height - 3, self.name)

        # draw connectors on terminals
        if self.terminalCLicked == Terminal.terminal1:
            brush = QPen()
            brush.setWidth(3)
            brush.setColor(Qt.GlobalColor.blue)
            painter.setPen(brush)
            painter.drawEllipse(self.width // 2 - 3, 0, 7, 7)  # terminal 1
        else:
            painter.drawEllipse(self.width // 2 - 3, 0, 7, 7)  # terminal 1

        # draw selection box
        if self.isSelected():
            painter.setPen(QPen(Qt.GlobalColor.red, 0.3, Qt.PenStyle.DashLine))
            painter.drawRect(self.boundingRect())

    def mousePressEvent(self, event) -> None:
        self.brush.setColor(Qt.GlobalColor.gray)
        if self.terminalLength - 5 <= event.pos().y() <= self.terminalLength + 8 \
                and self.width // 2 - 3 <= event.pos().x() <= self.width + 8:
            self.terminalCLicked = Terminal.terminal1
            # self.signals.terminalClicked.emit(event.pos(), 1)
            self.terminal_click_slot(event.pos(), 1)
        else:
            self.terminalCLicked = Terminal.none

        # print(self.terminalCLicked.name)
        self.update()

        # emit selected
        self.component_click_slot()

    def terminal_click_slot(self, terminal_position, terminal_id):
        self.signals.terminalClicked.emit(terminal_position, terminal_id)

    def component_click_slot(self):
        self.signals.componentSelected.emit()

    def hoverLeaveEvent(self, event) -> None:
        self.brush.setColor(Qt.GlobalColor.darkRed)

    def set_name(self, name):
        self.name = name

    def boundingRect(self):
        return QRectF(
            -self.padding,
            -self.padding,
            self.width + (2 * self.padding),
            self.height + (2 * self.padding),
        )
