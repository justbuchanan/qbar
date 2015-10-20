from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtCore import Qt, QPointF, QSize, QRectF
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle
from PyQt5 import QtCore
import psutil
from qbar.items.periodic_bar_item import PeriodicBarItem
from qbar.horizontal_bar_graph import *


class MulticoreCpuBarItem(PeriodicBarItem):
    def __init__(self, interval=0.2):
        super().__init__(icon='cpu', interval=interval)
        self._graph = HorizontalBarGraph()
        self.layout().addWidget(self._graph)
        self.text_widget.setParent(None)

    def refresh(self):
        cores = [v / 100.0 for v in psutil.cpu_percent(percpu=True)]
        self.content_changed.emit(cores)

    def set_content(self, cores):
        self._graph.values = cores
