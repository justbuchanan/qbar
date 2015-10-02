from qbar.items.periodic_bar_item import PeriodicBarItem
from qbar.horizontal_bar_graph import *
from qbar.font_awesome import *
from qbar.masked_icon import *
import psutil
import collections


## Draws a horizontal bar graph showing current memory usage
class MemoryBarItem(PeriodicBarItem):
    def __init__(self,icon=None, interval=2, show_swap=False):
        if icon == None:
            icon = MaskedImageIcon('images/ram3.png')
        super().__init__(icon=icon, interval=interval)
        self._graph = HorizontalBarGraph()
        self.layout().insertWidget(1, self._graph)
        self._show_swap = show_swap
        # self.text_widget.setParent(None)

    @property
    def show_swap(self):
        return self._show_swap

    def refresh(self):
        values = []

        pct = psutil.virtual_memory().percent / 100.0
        values.append(pct)

        if self.show_swap:
            swap = psutil.swap_memory()
            swap_pct = float(swap.percent) / 100.0
            values.append(swap_pct)

        self._graph.values = values
