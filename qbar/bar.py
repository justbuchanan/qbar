from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from qbar.bar_item import *
from qbar.items import *



# Bar that is shown on a single monitor
class Bar(QWidget):

    def __init__(self, items=[], parent=None, spacing=15):
        super().__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._spacing = spacing

        # Stay on top of other windows
        flags = QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint
        self.setWindowFlags(flags)

        # We're not running until a call to start() has been made
        self._running = False

        # setup layout
        layout = QtWidgets.QHBoxLayout()
        inset = self.spacing
        layout.setContentsMargins(inset,0,inset,0)
        layout.setSpacing(self.spacing)
        self.setLayout(layout)

        # Add bar items
        self.items = items

    @property
    def spacing(self):
        return self._spacing
    

    @property
    def running(self):
        return self._running
    

    @property
    def items(self):
        return self._items
    @items.setter
    def items(self, values):
        if self.running:
            # turn off the current items
            if self.items != None:
                for item in self.items: item.stop()
            # start the new items running
            if values != None:
                for item in values: item.start()

        # remove old items
        while self.layout().count():
            w = self.layout().takeAt(0).widget()
            if w != None:
                w.setParent(None)

        self._items = values

        for item in self.items:
            if isinstance(item, SpacerBarItem):
                self.layout().addStretch()
            else:
                self.layout().addWidget(item)

    def start(self):
        for item in self.items:
            item.start()
        self._running = True

    def stop(self):
        for item in self.items:
            item.stop()
        self._running = False
