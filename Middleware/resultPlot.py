from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from Middleware.circuitSimulationMiddleware import ResultPlot

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg


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
        self.plot(result.x_axis, result.y_axis)

    def plot(self, x, y):
        print("plotting")
        print(f"x: {x}")
        print(f"y: {y}")
        self.axes.clear()
        self.axes.plot(x, y)
        self.canvas.draw()  # Update the canvas to reflect the changes
        self.canvas.flush_events()  # Ensure the GUI is updated if necessary

# class MplCanvas(QWidget):
#     def __init__(self, result: ResultPlot, parent=None, width=5, height=5, dpi=100):
#         super(MplCanvas, self).__init__()
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
#         self.canvas = FigureCanvasQTAgg(fig)
#         layout = QVBoxLayout()
#         self.setLayout(layout)
#         layout.addWidget(self.canvas)
#         # super().__init__()
#         self.plot(result.x_axis, result.y_axis)
#
#     def plot(self, x, y):
#         print("plotting")
#         print(f"x:        {x}")
#         print(f"y:        {y}")
#         self.axes.clear()
#         self.axes.plot(x, y)
#         self.show()
#         self.update()
#         # self.draw()


# plotView = MplCanvas(width=5, height=5, dpi=100)
