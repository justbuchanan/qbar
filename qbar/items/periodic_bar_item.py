from qbar.items.simple_bar_item import SimpleBarItem
from PyQt5.QtCore import QTimer


# A SimpleBarItem that periodically updates its content
class PeriodicBarItem(SimpleBarItem):
    ## @interval is in seconds (may be partial)
    def __init__(self, icon=None, text="", interval=2):
        super().__init__(icon, text)
        self._timer = QTimer(self)
        self._timer.setInterval(interval * 1000) # convert to ms
        self._timer.timeout.connect(self.refresh)
        self._timer.start()

    def refresh(self):
        pass
