from PyQt6 import QtWidgets, QtCore
from PyQt6.sip import wrappertype

# from utils.components import QHLine


class ComponentsPane(QtWidgets.QWidget):
    class Signals(QtCore.QObject):
        """
        An Object class to organise all signals that would be emitted from the ComponentsPane
        """

        componentSelected = QtCore.pyqtSignal(wrappertype)

    def __init__(self, parent=None):
        super(ComponentsPane, self).__init__(parent)

        # making sure that the components' pane is not any smaller than 250px
        self.setMinimumWidth(250)

        # vertical box layout to arrange everything vertically
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)

        # add search box to the top of the components list
        self.searchBox = QtWidgets.QLineEdit()
        self.searchBox.setPlaceholderText("Search component or category")
        # self.searchBox.textChanged.connect(self.onSearchBoxTextChange)
        self.layout.addWidget(self.searchBox)
        self.layout.setAlignment(self.searchBox, QtCore.Qt.AlignmentFlag.AlignTop)

        # add a line separator between the search bar and the rest
        # self.layout.addWidget(QHLine())

        # creating a dropdown menu used to select component category
        self.componentCategory = QtWidgets.QComboBox()
        self.componentCategory.setPlaceholderText("Choose a component category")

        # sets the initial state of the components' category to "All" to display all components from the start
        self.componentCategory.setCurrentText("All")

        # adding stretch to the bottom to push all the components up
        self.layout.addStretch()
        # using the vertical box layout as the layout of the component pane
        self.setLayout(self.layout)
