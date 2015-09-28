from PyQt5.QtGui import QPainter, QPainterPath, QPalette
from PyQt5.QtCore import Qt, QPointF, QSize
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle
from PyQt5 import QtCore


class LineGraph(QWidget):
    def __init__(self, datapoints):
        super().__init__()
        self._datapoints = datapoints
        self.setMinimumSize(QSize(20, 10))

    # A collection of values between 0 and 1 to draw on the graph.  The values
    # are ordered from oldest to newest.
    @property
    def values(self):
        return self._values
    @values.setter
    def values(self, values):
        self._values = values
        self.update()

    ## The max number of datapoints this graph shows at once.  This determines
    # the drawing width relative to the width of the graph.
    @property
    def datapoints(self):
        return self._datapoints

    def paintEvent(self, event):
        # Draw backgrounds according to css
        styleOpt = QStyleOption()
        styleOpt.initFrom(self)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        self.style().drawPrimitive(QStyle.PE_Widget, styleOpt, p, self)

        if self.values == None or len(self.values) == 0: return

        r = self.rect()
        dx = r.width() / float(self.datapoints)

        # Build a path from the readings
        path = QPainterPath()
        path.moveTo(r.bottomRight())
        i = 0
        for reading in reversed(self.values):
            pt = QPointF(r.width() - i*dx, (1.0 - reading) * r.height())
            path.lineTo(pt)
            i = i + 1
        path.lineTo(path.currentPosition().x(), r.height())
        path.closeSubpath()

        # Use foreground color for graph
        gcolor = styleOpt.palette.color(QPalette.Text)
        p.setBrush(gcolor)
        p.setPen(gcolor)
        p.drawPath(path)
