from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QPixmap, QPen, QPainter, QColor, QAction
from PyQt6.QtCore import QSize, Qt, QPoint

from Components.symbol import Symbol


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.canvas = QPixmap(QSize(400, 400))
        self.label = QLabel()
        self.previousPoint = None
        self.button = QPushButton("Click Me", self)
        self.test = Symbol()
        self.size = 1
        self.init_ui()

    def init_ui(self):
        # set up canvas view
        self.setFixedSize(400, 400)
        self.setWindowTitle("Test Canvas Only")
        self.canvas.fill(QColor(255, 255, 255))
        self.label.setPixmap(self.canvas)
        self.setCentralWidget(self.label)
        self.layout = QVBoxLayout(self.label)
        self.layout.addWidget(self.test)
        self.draw_symbol()

    def draw_symbol(self):
        painter = QPainter(self.canvas)
        pen = QPen()
        pen.setColor(QColor(Qt.GlobalColor.black))
        pen.setWidth(self.size)
        painter.setPen(pen)
        self.test.draw_border(painter, pen)

        self.label.setPixmap(self.canvas)
        self.size *= 2
        print("successful", self.size)

    def draw_line(self, position):
        painter = QPainter(self.canvas)
        pen = QPen()
        pen.setColor(QColor(Qt.GlobalColor.black))
        painter.setPen(pen)
        self.test.draw_border(painter, pen)

        if self.previousPoint:
            painter.drawLine(self.previousPoint.x(), self.previousPoint.y(),
                             position.x(), position.y())
        else:
            painter.drawPoint(position.x(), position.y())

        self.label.setPixmap(self.canvas)
        self.previousPoint = position

    def mouseMoveEvent(self, event) -> None:
        print(event.pos().x())
        self.draw_line(event.pos())

    def mousePressEvent(self, event) -> None:
        self.layout.addWidget(self.test)
        self.draw_symbol()


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
