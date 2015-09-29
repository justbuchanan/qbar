from qbar.items.periodic_bar_item import PeriodicBarItem
from qbar.font_awesome import *
import time


class DateTimeBarItem(PeriodicBarItem):
    def __init__(self, format="%H:%M %a", icon=FA_CLOCK_O, interval=2):
        super().__init__(icon, "Time", interval)
        self._format = format

    def refresh(self):
        self.text = time.strftime(self.format)

    @property
    def format(self):
        return self._format
