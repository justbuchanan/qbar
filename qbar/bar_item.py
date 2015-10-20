from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from qbar.font_awesome import *


# Abstract superclass for all items that appear in the Bar.
class BarItem(QWidget):

    def __init__(self):
        super().__init__()
        self._bar = None

    def start(self):
        pass
    def stop(self):
        pass

    @property
    def bar(self):
        return self._bar
    @bar.setter
    def bar(self, value):
        self._bar = value

    def __del__(self):
        self.stop()

    ## Override paintEvent() so css works as expected
    ## Subclasses should call this implementation before doing custom drawing
    def paintEvent(self, event):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)
