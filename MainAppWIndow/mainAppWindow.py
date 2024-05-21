from PyQt6.QtCore import QSize, QObject, pyqtSignal
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QApplication, QToolBar, QVBoxLayout

from MainAppWIndow.AttributesPane.attributesPane import AttributesPane
from MainAppWIndow.Canvas.canvas import MyGraphicsView

from MainAppWIndow.ComponentsPane.componentsPane import ComponentsPane
from MainAppWIndow.ResultsandErrorPane.ResultsandErrorPane import LogConsole

from Components.Logger import qt_handler


class MainWindow(QMainWindow):
    class Signals(QObject):
        simulate = pyqtSignal()

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
        self.logConsole = LogConsole()
        self.attributes_pane_and_log_console = QVBoxLayout()
        self.init_ui()
        self._create_toolbar()
        self._connect_signals()
        self.signals = self.Signals()
        # connect canvas to main window simulate signal
        self.canvas.signals.simulate.connect(self.signals.simulate)

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
        self.attributes_pane_and_log_console.addWidget(self.attributesPane, 3)
        self.attributes_pane_and_log_console.addWidget(self.logConsole, 1)
        # self.layout.addWidget(self.attributesPane, 1)
        self.layout.addLayout(self.attributes_pane_and_log_console)

        container = QWidget()
        container.setLayout(self.layout)

        self.setCentralWidget(container)

    def _connect_signals(self):
        # # connect canvas to main window simulate signal
        self.canvas.signals.simulationData.connect(self.on_data_received)
        # connect canvas component select to attribute pane
        self.canvas.signals.componentSelected.connect(self.on_canvas_component_select)
        self.canvas.signals.componentDeselected.connect(self.on_canvas_component_deselect)
        self.canvas.signals.wireSelected.connect(self.on_canvas_wire_select)
        self.canvas.signals.wireDeselected.connect(self.on_canvas_wire_deselect)
        self.attributesPane.signals.deleteComponent.connect(self.on_component_delete)
        self.attributesPane.signals.deleteWire.connect(self.on_wire_delete)

        # connect component pane component select to canvas
        self.componentPane.signals.componentSelected.connect(self.on_component_select)

        # connect log signal to results and error pane
        qt_handler.signals.log.connect(self.logConsole.on_log)

    def _create_toolbar(self):
        """Create a toolbar for the main window"""
        # creating a toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(self.toolbar)

        self._create_and_add_simulate_action()
        self._create_and_add_wire_tool_action()
        self._create_and_add_rotate_action()

    def on_canvas_component_select(self, component):
        self.attributesPane.on_canvas_component_select(component)

    def on_canvas_component_deselect(self):
        self.attributesPane.on_canvas_component_deselect()

    def on_canvas_wire_select(self, wire):
        self.attributesPane.on_canvas_wire_select(wire)

        # print("Thesis Maame")

    def on_canvas_wire_deselect(self):
        self.attributesPane.on_canvas_wire_deselect()
        # print("Thesis Papa")

    def on_component_select(self, component):
        self.canvas.add_component(component)

    def on_component_delete(self, unique_id):
        self.canvas.delete_component(unique_id)

    def on_wire_delete(self, unique_id):
        self.canvas.delete_wire(unique_id)
        # print("about to delete wire")

    def _create_and_add_simulate_action(self):
        """Create a simulate action and add it to the toolbar"""
        # add simulate action
        simulate_button = QAction(
            QIcon("../Assets/simulate-icon.png"), "Simulate", self
        )
        simulate_button.setStatusTip("Simulate circuit on canvas")
        simulate_button.triggered.connect(self.on_simulate)
        simulate_button.setCheckable(True)
        self.toolbar.addAction(simulate_button)

    def _create_and_add_wire_tool_action(self):
        """Create a wire tool action and add it to the toolbar"""
        # adding wire tool action to the toolbar
        wire_tool = QAction(QIcon("../Assets/wire-tool-icon.png"), "Wire", self)
        wire_tool.setStatusTip("Wire")
        wire_tool.triggered.connect(self._on_wire_tool_click)
        wire_tool.setCheckable(True)
        self.toolbar.addAction(wire_tool)

    def _create_and_add_rotate_action(self):
        """Create a rotate action and add it to the toolbar"""
        # add rotate action to toolbar
        rotate_action = QAction(QIcon("../Assets/rotate-icon.png"), "Rotate", self)
        rotate_action.triggered.connect(self.rotate_selected_component)
        self.toolbar.addAction(rotate_action)

    def _on_wire_tool_click(self, state: bool):
        self.canvas.on_wire_tool_click(state)

    def rotate_selected_component(self):
        self.canvas.rotate_selected_components()

    def on_simulate(self, state: bool):
        # self.signals.simulate.emit()
        self.canvas.on_simulate(state)

    def on_data_received(self, text):
        self.logConsole.on_log(text)


app = QApplication([])
window = MainWindow()
window.show()
with open("../Assets/styles/app.stylesheet.qss", "r") as f:
    styles = f.read()
    app.setStyleSheet(styles)
app.exec()
