import typing

from PyQt6.QtCore import Qt, QPoint, QRectF, QPointF, pyqtSignal
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QGraphicsItem, QWidget, QGraphicsItemGroup, QGraphicsObject


class Wire(QGraphicsItem):
    class Signals(QGraphicsObject):
        wireSelected = pyqtSignal(str)
        wireDeselected = pyqtSignal()

    def __init__(self, color, color_text, points=[]):
        super().__init__()
        self.wireID = ""
        self.wireName = ""
        self.wireColour = color
        self.wireColourText = color_text
        self.start = None  # where wire starts from
        self.end = None  # where wire ends
        self.connectedComponents = []
        self.colors = {"darkGreen": Qt.GlobalColor.darkGreen, "darkRed": Qt.GlobalColor.darkRed,
                       "blue": Qt.GlobalColor.blue, "gray": Qt.GlobalColor.gray}
        self.uiWire = WireDrawing()

        self.signal = self.Signals()
        # self.uiWire.signals.wireSelected.connect(self.on_wire_select)
        # self.uiWire.signals.wireDeselected.connect(self.on_wire_deselect)
        # self.connect_signals()

        # trying something new
        self.points = points

        self.width = 200
        self.height = 1000
        self.terminalLength = 5
        self.padding = 10

        self.selected = False

        # item is selectable
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        # item can be dragged
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        # item can be highlighted
        self.hoveredTerminal = None
        self.setAcceptHoverEvents(True)

        self.signals = self.Signals()
        # self.signals.wireSelected.connect(self.emit_signal)
        # self.connect_signals()

    def set_color(self, text, color):
        self.wireColour = color
        self.wireColourText = text

    def connect_signals(self):
        self.signals.wireSelected.emit(self.wireID)

    def paint(self, painter, option, widget: typing.Optional[QWidget] = ...) -> None:
        # painter = QPainter()
        # print("painting")
        # print(self.points)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(self.wireColour)
        pen.setWidth(20)
        painter.setPen(pen)

        # while len(self.points > 2):
        #     self.points = self.points[1:]

        if len(self.points) >= 2:
            # Define a pen for drawing the lines
            pen = QPen(self.wireColour)
            pen.setWidth(2)
            painter.setPen(pen)

            # Draw lines connecting the points
            for i in range(len(self.points) - 1):
                start_point = self.points[i]
                end_point = self.points[i + 1]
                painter.drawLine(start_point, end_point)

        # draw selection box
        if self.isSelected():
            painter.setPen(QPen(Qt.GlobalColor.red, 0.3, Qt.PenStyle.DashLine))
            painter.drawRect(self.boundingRect())

    def redraw(self):
        self.update()

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedChange:
            if value:
                # pass
                self.signals.wireSelected.emit(self.wireID)
                # self.emit_signal()
                print(self.wireColour)

            else:
                # pass
                self.signals.wireDeselected.emit()
            self.update()
        return super().itemChange(change, value)

    def calculate_line_bounding_rect(self, point1, point2):
        # Calculate minimum and maximum coordinates
        min_x = min(point1.x(), point2.x())
        max_x = max(point1.x(), point2.x())
        min_y = min(point1.y(), point2.y())
        max_y = max(point1.y(), point2.y())

        return QRectF(min_x, min_y, max_x - min_x, max_y - min_y)

    def boundingRect(self):
        return self.calculate_line_bounding_rect(self.points[0], self.points[1])

    def connect_signals2(self):
        try:
            self.uiWire.signals.wireSelected.connect(self.on_wire_select)
            self.uiWire.signals.wireDeselected.connect(self.on_wire_deselect)
        except Exception as e:
            print(e)

    def on_wire_select(self):
        print(f"wire clicked: {self.wireID}")
        self.signal.wireSelected.emit(self.wireID)

    def on_wire_deselect(self):
        self.signal.wireDeselected.emit()


class WireDrawing(QGraphicsItem):
    class Signals(QGraphicsObject):
        wireSelected = pyqtSignal()
        wireDeselected = pyqtSignal()

    def __init__(self, points=[QPoint(0, 0)]):
        super(WireDrawing, self).__init__()
        self.points = points

        self.width = 200
        self.height = 1000
        self.terminalLength = 5
        self.padding = 10

        self.selected = False

        # item is selectable
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        # item can be dragged
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        # item can be highlighted
        self.hoveredTerminal = None
        self.setAcceptHoverEvents(True)

        self.signals = self.Signals()
        # self.signals.wireSelected.connect(self.emit_signal)
        self.connect_signals(self.emit_signal)

    def connect_signals(self, emit_handler):
        self.signals.wireSelected.connect(emit_handler)

    def paint(self, painter, option, widget: typing.Optional[QWidget] = ...) -> None:
        # painter = QPainter()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(Qt.GlobalColor.darkGreen)
        pen.setWidth(20)
        painter.setPen(pen)

        # while len(self.points > 2):
        #     self.points = self.points[1:]

        if len(self.points) >= 2:
            # Define a pen for drawing the lines
            pen = QPen(Qt.GlobalColor.darkGreen)
            pen.setWidth(2)
            painter.setPen(pen)

            # Draw lines connecting the points
            for i in range(len(self.points) - 1):
                start_point = self.points[i]
                end_point = self.points[i + 1]
                painter.drawLine(start_point, end_point)

        # draw selection box
        if self.isSelected():
            painter.setPen(QPen(Qt.GlobalColor.red, 0.3, Qt.PenStyle.DashLine))
            painter.drawRect(self.boundingRect())

    def redraw(self):
        self.update()

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedChange:
            if value:
                self.signals.wireSelected.emit()
                # self.emit_signal()

            else:
                self.signals.wireDeselected.emit()
            self.update()
        return super().itemChange(change, value)

    def emit_signal(self):
        # self.signals.wireSelected.emit()
        print("emit called")

    # def mousePressEvent(self, event) -> None:
    #     if self.isSelected():
    #         self.signals.wireSelected.emit()
    #         print(self.signals.wireSelected.emit())
    #     else:
    #         self.signals.wireDeselected.emit()

    def calculate_line_bounding_rect(self, point1, point2):
        # Calculate minimum and maximum coordinates
        min_x = min(point1.x(), point2.x())
        max_x = max(point1.x(), point2.x())
        min_y = min(point1.y(), point2.y())
        max_y = max(point1.y(), point2.y())

        return QRectF(min_x, min_y, max_x - min_x, max_y - min_y)

        # # Calculate minimum and maximum coordinates
        # min_x = min(point1.x(), point2.x())
        # max_x = max(point1.x(), point2.x())
        # min_y = min(point1.y(), point2.y())
        # max_y = max(point1.y(), point2.y())
        #
        # # Calculate the center point of the line
        # center_x = (point1.x() + point2.x()) / 2
        # center_y = (point1.y() + point2.y()) / 2
        # center_point = QPointF(center_x, center_y)
        #
        # # Calculate width and height of the bounding rectangle
        # width = max_x - min_x
        # height = max_y - min_y
        #
        # # Create a QRectF for the bounding rectangle
        # line_rect = QRectF(center_point.x() - width / 2, center_point.y() - height / 2,
        #                    width, height)
        #
        # return line_rect

    def boundingRect(self):
        # return QRectF(
        #     -0.5 * self.padding,
        #     -0.5 * self.padding,
        #     self.width + (2 * self.padding),
        #     self.height + (2 * self.padding),
        # )
        return self.calculate_line_bounding_rect(self.points[0], self.points[1])


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
