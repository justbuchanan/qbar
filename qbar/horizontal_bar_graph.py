from PyQt5.QtGui import QPainter, QPainterPath, QPalette
from PyQt5.QtCore import Qt, QPointF, QSize, QRectF
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle
from PyQt5 import QtCore



class HorizontalBarGraph(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(20, 10)
        self._values = None

    @property
    def values(self):
        return self._values
    @values.setter
    def values(self, values):
        self._values = values
        self.update()

    def paintEvent(self, event):
        # Draw backgrounds according to css
        styleOpt = QStyleOption()
        styleOpt.initFrom(self)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        self.style().drawPrimitive(QStyle.PE_Widget, styleOpt, p, self)

        if self.values == None or len(self.values) == 0: return

        r = self.rect()

        gcolor = styleOpt.palette.color(QPalette.Text)
        p.setBrush(gcolor)
        p.setPen(gcolor)

        for i in range(len(self.values)):
            spacing = 4
            thickness = (r.height() - spacing*(len(self.values)-1)) / len(self.values)
            p.drawRect(QRectF(0, (thickness+spacing) * i, self.values[i]*r.width(), thickness))
