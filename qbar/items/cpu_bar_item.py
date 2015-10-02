from qbar.items.periodic_bar_item import PeriodicBarItem
from qbar.line_graph import LineGraph
from qbar.font_awesome import *
from qbar.masked_icon import *
import psutil
import collections


# Shows a graph of cpu usage over time
class CpuBarItem(PeriodicBarItem):
    ## @param datapoints the number of cpu samples to show in the graph
    #  @param interval how often to sample.
    #  The time period shown by the graph is 
    def __init__(self, icon=None, interval=0.5, datapoints=20):
        if icon == None:
            icon = MaskedImageIcon("images/cpu3.png")
        super().__init__(icon=icon, interval=interval)
        self._history = collections.deque(maxlen=datapoints)
        self._graph = LineGraph(datapoints)
        self.layout().addWidget(self._graph)
        self.text_widget.setParent(None)

    # Circular buffer of past cpu usage readings
    @property
    def history(self):
        return self._history

    def refresh(self):
        reading = psutil.cpu_percent() / 100.0
        self.history.append(reading)
        self._graph.values = self.history
