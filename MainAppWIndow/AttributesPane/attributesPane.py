from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.sip import wrappertype

# from utils.components import QHLine


class AttributesPane(QtWidgets.QWidget):
    class Signals(QtCore.QObject):
        """
        An Object class to organise all signals that would be emitted from the ComponentsPane
        """

        deleteComponent = pyqtSignal(str)

    def __init__(self, parent=None):
        # making sure that the components' pane is not any smaller than 250px
        super(AttributesPane, self).__init__(parent)
        self.setMinimumWidth(250)

        # vertical box layout to arrange everything vertically
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.layout.addStretch()
        # using the vertical box layout as the layout of the component pane
        self.setLayout(self.layout)