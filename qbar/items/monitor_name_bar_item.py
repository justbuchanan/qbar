from qbar.items.simple_bar_item import *
from qbar.font_awesome import *


class MonitorNameBarItem(SimpleBarItem):
    def __init__(self, icon=FA_DESKTOP):
        super().__init__(icon)

    @BarItem.bar.setter
    def bar(self, value):
        BarItem.bar.fset(self, value)
        self.text = "<Monitor Name>" if value == None else self.bar.monitor_name
