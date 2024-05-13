import typing

from PyQt6.QtCore import Qt, QPoint, QRectF
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QGraphicsItem, QWidget, QGraphicsItemGroup


class Wire:
    def __init__(self):
        self.wireID = ""
        self.wireName = ""
        self.wireColour = Qt.GlobalColor.darkGreen
        self.start = None  # where wire starts from
        self.end = None  # where wire ends
        self.connectedComponents = []


class WireDrawing(QGraphicsItem):
    def __init__(self, points):
        super(WireDrawing, self).__init__()
        self.points = points

        self.width = 20
        self.height = 100
        self.terminalLength = 5
        self.padding = 10

        self.selected = False

        # item is selectable
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        # item can be dragged
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)

        # item can be highlighted
        self.hoveredTerminal = None
        self.setAcceptHoverEvents(True)

    def paint(self, painter, option, widget: typing.Optional[QWidget] = ...) -> None:
        print("testt")
        print(len(self.points))
        # painter = QPainter()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(Qt.GlobalColor.darkGreen)
        pen.setWidth(20)
        painter.setPen(pen)

        if len(self.points) >= 2:
            # Define a pen for drawing the lines
            pen = QPen(Qt.GlobalColor.darkGreen)
            pen.setWidth(2)
            painter.setPen(pen)
            print("test 2")

            # Draw lines connecting the points
            for i in range(len(self.points) - 1):
                start_point = self.points[i]
                end_point = self.points[i + 1]
                painter.drawLine(start_point, end_point)
                print("test 3 ", i)

        # draw selection box
        if self.isSelected():
            painter.setPen(QPen(Qt.GlobalColor.red, 0.3, Qt.PenStyle.DashLine))
            painter.drawRect(self.boundingRect())

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        print("hoooover")

    def redraw(self):
        self.update()

    def boundingRect(self):
        return QRectF(
            -0.5 * self.padding,
            -0.5 * self.padding,
            self.width + (2 * self.padding),
            self.height + (2 * self.padding),
        )


class ConnectedLinesGroup(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()
        # self.setFlags(QGraphicsItemGroup.ItemIsSelectable | QGraphicsItemGroup.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsMovable)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setSelected(True)
        else:
            QGraphicsItemGroup.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setSelected(False)
        else:
            QGraphicsItemGroup.mouseReleaseEvent(self, event)
