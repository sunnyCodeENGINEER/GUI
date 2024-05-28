from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(QWidget):
    def __init__(self, parent=None, width=5, height=5, dpi=100):
        super(MplCanvas, self).__init__()
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(fig)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.canvas)
        # super().__init__()
        self.plot([1, 2, 8, 3], [9, 3, 1, 6])

    def plot(self, x, y):
        self.axes.clear()
        self.axes.plot(x, y)
        # self.draw()
