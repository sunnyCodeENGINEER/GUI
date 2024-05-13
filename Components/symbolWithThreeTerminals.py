import typing
from enum import Enum

from PyQt6.QtCore import pyqtSignal, QPointF, QRectF, QPoint, Qt
from PyQt6.QtGui import QPainter, QPen, QBrush, QImage, QFont
from PyQt6.QtWidgets import QGraphicsObject, QWidget, QGraphicsItem


class Terminal(Enum):
    none = None
    terminal1 = 1
    terminal2 = 2
    terminal3 = 3


class SymbolWithThreeTerminals(QGraphicsItem):
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

        self.image_path = "../Assets/ResistorBG.png"
        self.image = QImage(self.image_path)

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
        point_c = QPointF(point_b.x(), point_b.y() + self.height - (2 * self.terminalLength))
        point_d = QPointF(point_a.x(), point_a.y() + self.height - (2 * self.terminalLength))

        # Draw the edges of the rectangle in the resistor
        painter.drawLine(point_a, point_b)
        painter.drawLine(point_b, point_c)
        painter.drawLine(point_c, point_d)
        painter.drawLine(point_d, point_a)

        t1_a = QPointF(0, self.height // 2)
        t1_b = QPointF(self.terminalLength, self.height // 2)
        t2_a = QPointF(self.width - self.terminalLength, self.height // 2)
        t2_b = QPointF(self.width, self.height // 2)
        t3_a = QPoint(self.width // 2 - 3, self.height - (2 * self.terminalLength))
        t3_b = QPoint(self.width // 2 - 3, self.height - (1 * self.terminalLength))

        # draw terminals from their endpoints
        painter.drawLine(t1_a, t1_b)
        painter.drawLine(t2_a, t2_b)
        painter.drawLine(t3_a, t3_b)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # draw image
        scaled_image = self.image.scaled(80, 80)
        painter.drawImage(self.terminalLength, 1, scaled_image)

        # draw component name
        font = QFont("Arial", 8)  # Specify font family and font size (e.g., 12 points)
        painter.setFont(font)
        painter.drawText(10, self.height - 3, self.name)

        # draw connectors on terminals
        if self.terminalCLicked == Terminal.terminal1:
            painter.drawEllipse(self.width, (self.height // 2) - 4, 7, 7)  # terminal 2
            painter.drawEllipse(self.width // 2 - 6, self.height - self.terminalLength, 7, 7)  # terminal 3
            brush = QPen()
            brush.setWidth(3)
            brush.setColor(Qt.GlobalColor.blue)
            painter.setPen(brush)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.drawEllipse(-self.terminalLength - 3, (self.height // 2) - 4, 7, 7)  # terminal 1
        elif self.terminalCLicked == Terminal.terminal2:
            painter.drawEllipse(-self.terminalLength - 3, (self.height // 2) - 4, 7, 7)  # terminal 1
            painter.drawEllipse(self.width // 2 - 6, self.height - self.terminalLength, 7, 7)  # terminal 3
            brush = QPen()
            brush.setWidth(3)
            brush.setColor(Qt.GlobalColor.blue)
            painter.setPen(brush)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.drawEllipse(self.width, (self.height // 2) - 4, 7, 7)  # terminal 2
        elif self.terminalCLicked == Terminal.terminal3:
            painter.drawEllipse(-self.terminalLength - 3, (self.height // 2) - 4, 7, 7)  # terminal 1
            painter.drawEllipse(self.width, (self.height // 2) - 4, 7, 7)  # terminal 2
            brush = QPen()
            brush.setWidth(3)
            brush.setColor(Qt.GlobalColor.blue)
            painter.setPen(brush)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.drawEllipse(self.width // 2 - 6, self.height - self.terminalLength, 7, 7)  # terminal 3
        else:
            painter.drawEllipse(-self.terminalLength - 3, (self.height // 2) - 4, 7, 7)  # terminal 1
            painter.drawEllipse(self.width, (self.height // 2) - 4, 7, 7)  # terminal 2
            painter.drawEllipse(self.width // 2 - 6, self.height - self.terminalLength, 7, 7)  # terminal 3

        # draw selection box
        if self.isSelected():
            painter.setPen(QPen(Qt.GlobalColor.red, 0.3, Qt.PenStyle.DashLine))
            painter.drawRect(self.boundingRect())

    def mousePressEvent(self, event) -> None:
        self.brush.setColor(Qt.GlobalColor.gray)
        if -self.terminalLength - 3 <= event.pos().x() <= -self.terminalLength + 8 \
                and self.height // 2 - 3 <= event.pos().y() <= self.height // 2 + 8:
            self.terminalCLicked = Terminal.terminal1
            # emit signal
            # self.signals.terminalClicked.emit(event.pos(), 1)
            self.terminal_click_slot(event.pos(), 1)
        elif self.width - 3 <= event.pos().x() <= self.width + 8 \
                and self.height // 2 - 3 <= event.pos().y() <= self.height // 2 + 8:
            self.terminalCLicked = Terminal.terminal2
            # emit signal
            # self.signals.terminalClicked.emit(event.pos(), 2)
            self.terminal_click_slot(event.pos(), 2)
        elif self.width // 2 - 8 <= event.pos().x() <= self.width // 2 + 8 \
                and self.height - self.terminalLength - 4 <= event.pos().y() <= self.height - self.terminalLength + 8:
            self.terminalCLicked = Terminal.terminal3
            # emit signal
            # self.signals.terminalClicked.emit(event.pos(), 3)
            self.terminal_click_slot(event.pos(), 3)
        else:
            self.terminalCLicked = Terminal.none

        self.update()
        # print(self.terminalCLicked.name)

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
