from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle
from qbar.font_awesome import *


# Abstract superclass for all items that appear in the Bar.
class BarItem(QWidget):

    def start(self):
        pass
    def stop(self):
        pass

    ## Override paintEvent() so css works as expected
    ## Subclasses should call this implementation before doing custom drawing
    def paintEvent(self, event):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)
