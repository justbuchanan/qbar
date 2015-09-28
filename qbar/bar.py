from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget

from qbar.bar_item import *
from qbar.items.spacer_bar_item import *



# Bar that is shown on a single monitor
class Bar(QWidget):
    def __init__(self, items=[], parent=None):
        super().__init__(parent)

        # Stay on top of other windows
        self.setWindowFlags(QtCore.Qt.X11BypassWindowManagerHint)

        # Add bar items
        self._items = items
        layout = QtWidgets.QHBoxLayout()
        for item in self.items:
            if isinstance(item, SpacerBarItem):
                layout.addStretch()
            else:
                layout.addWidget(item)
        self.setLayout(layout)

    @property
    def items(self):
        return self._items

    def start(self):
        for item in self.items:
            item.start()

    def stop(self):
        for item in self.items:
            item.stop()
