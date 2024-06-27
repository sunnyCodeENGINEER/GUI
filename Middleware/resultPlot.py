import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from Middleware.circuitSimulationMiddleware import ResultPlot

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

import matplotlib.pyplot as plt
from PySpice.Plot.BodeDiagram import bode_diagram


class MplCanvas(QWidget):
    def __init__(self, result, parent=None, width=5, height=5, dpi=100):
        super(MplCanvas, self).__init__(parent)

        # Create a Matplotlib figure and axis
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        # Create a canvas and add it to the layout
        self.canvas = FigureCanvasQTAgg(fig)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.canvas)

        # Plot the initial data
        # self.plot(result.x_axis, result.y_axis)

    def plot(self, x, y):
        # print("plotting")
        # print(f"x: {x}")
        # print(f"y: {y}")
        self.axes.clear()
        self.axes.plot(x, y)
        self.canvas.draw()  # Update the canvas to reflect the changes
        self.canvas.flush_events()  # Ensure the GUI is updated if necessary
        self.show()

    def plot_ac(self, frequency, node):
        bode_diagram(axes=self.axes,
                     frequency=frequency,
                     gain=20*np.log10(np.absolute(node)),
                     phase=np.angle(node, deg=False),
                     marker='-',
                     color='blue',
                     linestyle='-'
                     )
        plt.tight_layout()
        # self.show()

