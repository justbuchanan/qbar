from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle
from PyQt5 import QtCore

from qbar.items.periodic_bar_item import PeriodicBarItem
from qbar.line_graph import LineGraph
import psutil
import collections



# Shows a graph of cpu usage over time
class CpuBarItem(PeriodicBarItem):
    def __init__(self, interval=0.5, datapoints=20):
        super().__init__(icon="CPU", interval=interval)
        self._history = collections.deque(maxlen=datapoints)
        self._graph = LineGraph(datapoints)
        self.layout().addWidget(self._graph)


    # Circular buffer of past cpu usage readings
    @property
    def history(self):
        return self._history

    def refresh(self):
        reading = psutil.cpu_percent() / 100.0
        self.history.append(reading)
        self._graph.values = self.history
