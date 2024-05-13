from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QApplication

from MainAppWIndow.AttributesPane.attributesPane import AttributesPane
from MainAppWIndow.Canvas.canvas import MyGraphicsView

from MainAppWIndow.ComponentsPane.componentsPane import ComponentsPane


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout = None
        self.attributesPane = None
        # self.layout = None
        # self.canvas = None
        # self.componentPane = None
        self.componentPane = ComponentsPane()  # component pane
        self.canvas = MyGraphicsView()  # canvas
        self.attributesPane = AttributesPane()
        self.init_ui()
        self._connect_signals()

    def init_ui(self):
        self.setWindowTitle("NGSpice GUI 0.2")
        self.resize(1000, 800)
        self.setMinimumWidth(1000)
        self.setMinimumHeight(800)

        # self.componentPane = ComponentsPane()  # component pane
        # self.canvas = MyGraphicsView()  # canvas
        # self.attributesPane = AttributesPane()

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)
        self.layout.addWidget(self.componentPane, 1)
        self.layout.addWidget(self.canvas, 4)
        self.layout.addWidget(self.attributesPane, 1)

        container = QWidget()
        container.setLayout(self.layout)

        self.setCentralWidget(container)

    def _connect_signals(self):
        # connect canvas component select to attribute pane
        self.canvas.signals.componentSelected.connect(self.on_canvas_component_select)
        self.attributesPane.signals.deleteComponent.connect(self.on_component_delete)

        # connect component pane component select to canvas
        self.componentPane.signals.componentSelected.connect(self.on_component_select)

    def on_canvas_component_select(self, component):
        self.attributesPane.on_canvas_component_select(component)

    def on_component_select(self, component):
        self.canvas.add_component(component)

    def on_component_delete(self, unique_id):
        self.canvas.delete_component(unique_id)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
