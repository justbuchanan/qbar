from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from qbar.bar_item import *
from qbar.items import *


# Bar that is shown on a single monitor
class Bar(QWidget):

    def __init__(self, monitor_name=None, items=[], parent=None, height=30, position="top", spacing=15):
        super().__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._spacing = spacing
        self._height = height
        self._position = position

        # Stay on top of other windows
        flags = QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint
        self.setWindowFlags(flags)

        # We're not running until a call to start() has been made
        self._running = False

        # setup layout
        layout = QtWidgets.QHBoxLayout()

        # Keep bar from expanding too much due to an abundance of bar items
        layout.setSizeConstraint(QLayout.SetMaximumSize)

        inset = self.spacing
        layout.setContentsMargins(inset,0,inset,0)
        layout.setSpacing(self.spacing)
        self.setLayout(layout)

        self._monitor_name = monitor_name

        # Add bar items
        self._items = []
        self.items = items

        # set geometry
        geom = Bar.frame_for_monitor(self.monitor_name)
        y = geom.height() - height if self.position == "bottom" else 0
        self.setGeometry(geom.x(), y, geom.width(), self.height)


    @property
    def monitor_name(self):
        return self._monitor_name


    ## @param monitor_name If None, uses the primary monitor
    @classmethod
    def frame_for_monitor(self, monitor_name=None):
        desktop = QApplication.desktop()
        # x = 0
        for i in range(desktop.screenCount()):
            screen = QApplication.screens()[i]
            # geom = desktop.screenGeometry(i)
            if monitor_name == None and i == desktop.primaryScreen() or screen.name() == monitor_name:
                # print("x for monitor '%s' = %d" % (monitor_name, x))
                # return QRectF(x, 0, geom.width(), geom.height())
                return screen.geometry()
            # x += geom.width()

        raise KeyError("Unable to find monitor named %s" % monitor_name)


    @property
    def spacing(self):
        return self._spacing

    @property
    def height(self):
        return self._height

    @property
    def position(self):
        return self._position


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

        for item in self.items: item.bar = None
        for item in values: item.bar = self

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
