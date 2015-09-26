from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtCore import Qt, QPointF

from qbar.items.periodic_bar_item import PeriodicBarItem
# from qbar.font_awesome import *
import psutil
import collections


# Shows a graph of cpu usage over time
class CpuBarItem(PeriodicBarItem):
    def __init__(self, interval=0.5, datapoints=20):
        self._history = collections.deque(maxlen=datapoints)
        super().__init__(interval=interval)
        self.icon = "CPU"

    # Circular buffer of past cpu usage readings
    @property
    def history(self):
        return self._history

    def refresh(self):
        reading = psutil.cpu_percent() / 100.0
        self.history.append(reading)
        self.update() # redraw graph

    # Draws a line graph showing cpu utilization over time
    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)

        r = self.rect()
        dx = r.width() / float(self.history.maxlen)

        # Build a path from the cpu readings
        path = QPainterPath()
        path.moveTo(r.bottomRight())
        i = 0
        for reading in reversed(self.history):
            pt = QPointF(r.width() - i*dx, (1.0 - reading) * r.height())
            path.lineTo(pt)
            i = i + 1
        path.lineTo(path.currentPosition().x(), r.height())
        path.closeSubpath()

        # p.fillRect(r, Qt.gray)

        gcolor = Qt.green
        p.setBrush(gcolor)
        p.setPen(gcolor)
        p.drawPath(path)
