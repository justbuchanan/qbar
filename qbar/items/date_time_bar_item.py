from qbar.items.periodic_bar_item import PeriodicBarItem
from qbar.font_awesome import *
import time


class DateTimeBarItem(PeriodicBarItem):
    def __init__(self, format="%H:%M %a", interval=2):
        self._format = format
        super().__init__(FontAwesomeIcon(FA_CLOCK_O), "Time", interval)

    def refresh(self):
        self.text = time.strftime(self.format)

    @property
    def format(self):
        return self._format
