import numpy as np
from PyQt6.QtCore import QSize, QObject, pyqtSignal
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QApplication, QToolBar, QVBoxLayout, QLineEdit, \
    QPushButton, QInputDialog, QMessageBox

from MainAppWIndow.AttributesPane.attributesPane import AttributesPane
from MainAppWIndow.Canvas.canvas import MyGraphicsView

from MainAppWIndow.ComponentsPane.componentsPane import ComponentsPane
from MainAppWIndow.ResultsandErrorPane.ResultsandErrorPane import LogConsole

from Components.logger import qt_log_handler
# from Components.logger.qt_handler import QtLogHandler
from Middleware.circuitSimulationMiddleware import ResultPlot
from Middleware.resultPlot import MplCanvas

import matplotlib.pyplot as plt


class MainWindow(QMainWindow):
    class Signals(QObject):
        simulate = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout = None
        self.attributesPane = None
        self.componentPane = ComponentsPane()  # component pane
        self.canvas = MyGraphicsView()  # canvas
        self.plotData = ResultPlot("", [], [], "", "")
        self.plotView = MplCanvas(self.plotData, width=5, height=5, dpi=100)
        self.attributesPane = AttributesPane()
        self.logConsole = LogConsole()
        self.attributes_pane_and_log_console = QVBoxLayout()
        self.canvas_and_plot = QVBoxLayout()
        self.init_ui()
        self._create_toolbar()
        self._connect_signals()
        self.signals = self.Signals()
        self.isSimulating = False

        # connect canvas to main window simulate signal
        self.canvas.signals.simulate.connect(self.signals.simulate)

    def init_ui(self):
        self.setWindowTitle("NGSpice GUI 0.2")
        self.resize(1000, 800)
        self.setMinimumWidth(1000)
        self.setMinimumHeight(800)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)
        self.layout.addWidget(self.componentPane, 1)
        # self.layout.addWidget(self.canvas, 4)
        self.canvas_and_plot.addWidget(self.canvas)
        # if self.plotData:
        self.canvas_and_plot.addWidget(self.plotView)
        self.plotView.hide()
        # self.canvas_and_plot.addWidget(plotView)
        self.layout.addLayout(self.canvas_and_plot, 4)
        self.attributes_pane_and_log_console.addWidget(self.attributesPane, 3)
        self.attributes_pane_and_log_console.addWidget(self.logConsole, 1)
        self.layout.addLayout(self.attributes_pane_and_log_console)

        container = QWidget()
        container.setLayout(self.layout)

        self.setCentralWidget(container)

    def _connect_signals(self):
        # # connect canvas to main window simulate signal
        self.canvas.signals.simulationData.connect(self.on_data_received)
        self.canvas.signals.simulationResult.connect(self.result_received)
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
        qt_log_handler.signals.log.connect(self.logConsole.on_log)

    def result_received(self, result):
        print("results here")
        # self.plotView.plot(result.x_axis, result.y_axis)
        #
        if self.canvas.analysisType == "Operating Point":
            _ = result[0]
            self.canvas.operating_point_result(_)
            # for node in _.nodes.values():
            #     wire = self.canvas.wires.get(str(node))
            #     try:
            #         print(node)
            #         print(wire.wireValue)
            #         # wire.set_value(float(node))
            #         # wire.wireValue = float(node)
            #         print("======")
            #
            #         # print(wire.wireValue)
            #         # wire.redraw()
            #     except Exception as e:
            #         print(e)
                # wire.redraw()
            return

        if self.canvas.analysisType == "AC Analysis":
            # return
            for node in result:
                wire = self.canvas.wires.get(node.plot_label)
                legend_string = wire.wireName
                plt.title(f'Bode Diagram of {self.canvas.circuitName}')
                fig, axes = plt.subplots(2, figsize=(20, 10))
                self.bode_diagram2(axes=axes,
                                   frequency=node.x_axis,
                                   gain=20 * np.log10(np.absolute(node.y_axis)),
                                   phase=np.angle(node.y_axis, deg=False),
                                   marker='-',
                                   label=legend_string)
                pass
            return

        self.plotView.axes.clear()
        if self.canvas.analysisType == "DC Sweep":
            for node in result:
                self.plotView.axes.plot(node.x_axis, node.y_axis, label=node.plot_label)

            self.plotView.axes.set_title(f'DC Sweep Analysis of {self.canvas.circuitName}')
            # self.plotView.axes.xlabel("input voltage (V)")
            # self.plotView.axes.ylabel(f'output voltage (V)')
            # self.plotView.xlabel("input voltage (V)")
            # self.plotView.ylabel("output voltage (V)")
            self.plotView.axes.grid(True)
            self.plotView.axes.legend()
            self.plotView.canvas.draw()
            return

        self.plotView.show()
        self.plotView.axes.clear()
        print("===================")
        for node in result:
            # self.plotView.axes.plot(result.x_axis, result.y_axis)

            _ = self.canvas.wires.get(node.plot_label)
            legend_string = _.wireName
            # print(wire)
            # legend_string = wire.wireName
            self.plotView.axes.plot(node.x_axis, node.y_axis, label=legend_string)
        # self.plotView = MplCanvas(result)
        self.plotView.axes.set_title(f'Transient Analysis of {self.canvas.circuitName}')
        # self.plotView.axes.set_xlabel("Voltage")
        # self.plotView.axes.set_ylabel("Time")
        # self.plotView.xlabel("Voltage")
        # self.plotView.ylabel("Time")
        self.plotView.axes.grid(True)
        self.plotView.axes.legend()
        self.plotView.canvas.draw()

        # self.plotView.update()
        # self.update()
        pass

    def bode_diagram2(self, axes, frequency, gain, phase, marker, label):
        ax_gain, ax_phase = axes
        ax_gain.plot(frequency, gain, marker, label=label)
        ax_gain.set_xscale('log')
        ax_gain.set_ylabel('Gain (dB)')
        ax_gain.legend()
        ax_gain.grid(True, which='both', linestyle='--', linewidth=0.5)

        ax_phase.plot(frequency, np.degrees(phase), marker, label=label)
        ax_phase.set_xscale('log')
        ax_phase.set_ylabel('Phase (degrees)')
        ax_phase.set_xlabel('Frequency (Hz)')
        ax_phase.legend()
        ax_phase.grid(True, which='both', linestyle='--', linewidth=0.5)

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

    def on_canvas_wire_deselect(self):
        self.attributesPane.on_canvas_wire_deselect()

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

    def _create_and_add_simulate_setting_action(self):
        """Create a simulate action and add it to the toolbar"""
        # add simulate action
        simulate_button = QAction(
            QIcon("../Assets/simulate-icon.png"), "Simulation Settings", self
        )
        simulate_button.setStatusTip("Set simulation settings")
        simulate_button.triggered.connect(self.on_simulation_setting)
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
        if state:
            if self.canvas.analysisType != "Operating Point":
                self.plotView.show()

        else:
            self.plotView.axes.clear()
            self.plotView.hide()

    def on_simulation_setting(self):
        pass

    def on_data_received(self, text):
        self.logConsole.on_log(text)


app = QApplication([])
window = MainWindow()
window.show()
with open("../Assets/styles/app.stylesheet.qss", "r") as f:
    styles = f.read()
    app.setStyleSheet(styles)
app.exec()
