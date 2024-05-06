from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QApplication

from MainAppWIndow.Canvas.canvas import MyGraphicsView

from MainAppWIndow.ComponentsPane.componentsPane import ComponentsPane


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout = None
        self.canvas = None
        self.componentPane = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("NGSpice GUI 0.2")
        self.resize(1000, 800)
        self.setMinimumWidth(1000)
        self.setMinimumHeight(800)

        self.componentPane = ComponentsPane()  # component pane
        self.canvas = MyGraphicsView()  # canvas

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)
        self.layout.addWidget(self.componentPane, 1)
        self.layout.addWidget(self.canvas, 4)

        container = QWidget()
        container.setLayout(self.layout)

        self.setCentralWidget(container)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
