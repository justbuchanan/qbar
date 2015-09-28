from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle
from PyQt5 import QtCore

from qbar.items.periodic_bar_item import PeriodicBarItem
from qbar.horizontal_bar_graph import *
from qbar.font_awesome import *
import psutil
import collections


class MemoryBarItem(PeriodicBarItem):
    def __init__(self, interval=2):
        super().__init__(icon="ram", interval=interval)
        self._graph = HorizontalBarGraph()
        self.layout().insertWidget(1, self._graph)
        # self.text_widget.setParent(None)

    def refresh(self):
        mem = psutil.virtual_memory()

        gb = 1024**3
        used = mem.used / gb
        total = mem.total / gb

        pct = used / total 

        pct = mem.percent / 100
        # self.text = "%.1f / %.1fgb" % (used, total)

        self._graph.values = [pct]

