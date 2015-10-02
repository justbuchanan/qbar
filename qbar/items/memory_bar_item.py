from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle
from PyQt5 import QtCore

from qbar.items.periodic_bar_item import PeriodicBarItem
from qbar.horizontal_bar_graph import *
from qbar.font_awesome import *
import psutil
import collections

from qbar.masked_icon import *


class MemoryBarItem(PeriodicBarItem):
    def __init__(self,icon=None, interval=2, show_swap=False):
        super().__init__(icon=icon, interval=interval)
        if icon == None:
            icon = MaskedImageIcon('images/ram3.png')
        self._graph = HorizontalBarGraph()
        self.layout().insertWidget(1, self._graph)
        self._show_swap = show_swap
        # self.text_widget.setParent(None)

    @property
    def show_swap(self):
        return self._show_swap
    

    def refresh(self):
        values = []

        mem = psutil.virtual_memory()
        gb = 1024**3
        used = mem.used / gb
        total = mem.total / gb
        pct = used / total 
        pct = float(mem.percent) / 100.0
        values.append(pct)
        # self.text = "%.1f / %.1fgb" % (used, total)

        if self.show_swap:
            swap = psutil.swap_memory()
            swap_pct = float(swap.percent) / 100.0
            values.append(swap_pct)

        self._graph.values = values
