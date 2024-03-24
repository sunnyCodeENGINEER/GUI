from PyQt6.QtCore import pyqtSignal, QPointF, QRectF
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QGraphicsObject, QWidget


class Symbol(QWidget):

    class Signals(QGraphicsObject):
        # signal sends (uniqueID, terminalIndex) as arguments.
        terminalClicked = pyqtSignal(str, int)
        componentMoved = pyqtSignal()
        componentSelected = pyqtSignal(str)
        componentDeselected = pyqtSignal(str)
        componentDataChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.width = 70
        self.height = 70
        self.terminalLength = 5
        self.padding = 7

    def draw_border(self, painter: QPainter, pen: QPen):
        # initialize painter
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

    def boundingRect(self):
        return QRectF(
            -self.padding,
            -self.padding,
            self.width + (2 * self.padding),
            self.height + (2 * self.padding),
        )

    # def getTerminalPositions(self) -> Tuple[QPointF, QPointF]:
    #     t1_pos = self.mapToScene(0, self.h // 2)
    #     t2_pos = self.mapToScene(self.w, self.h // 2)
    #     return t1_pos, t2_pos

