from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget

# Bar that is shown on a single monitor
class Bar(QWidget):
    def __init__(self, items=[], parent=None):
        super().__init__(parent)

        # Stay on top of other windows
        self.setWindowFlags(QtCore.Qt.X11BypassWindowManagerHint)

        # Add bar items
        self._items = items
        layout = QtWidgets.QHBoxLayout()
        layout.addStretch()
        for item in self.items:
            layout.addWidget(item)
        self.setLayout(layout)

    @property
    def items(self):
        return self._items
    
