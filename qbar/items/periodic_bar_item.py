from qbar.items.simple_bar_item import SimpleBarItem
from PyQt5.QtCore import QTimer, pyqtSignal


# A SimpleBarItem that periodically updates its content
class PeriodicBarItem(SimpleBarItem):

    content_changed = pyqtSignal(object)

    ## @interval is in seconds (may be partial)
    def __init__(self, icon=None, text="", interval=2):
        super().__init__(icon, text)
        self._interval = interval
        self._timer = None
        self.content_changed.connect(self.set_content)

    @property
    def interval(self):
        return self._interval
    
    def start(self):
        if not self._timer:
            self._timer = QTimer(self)
            self._timer.setInterval(self.interval * 1000) # convert to ms
            self._timer.timeout.connect(self.refresh)
            self._timer.start()
            self.refresh()

    def stop(self):
        if self._timer:
            self._timer.stop()
            self._timer = None

    # Refresh should fetch new contents, then emit the content_changed signal
    # with the processed content.
    # `self.content_changed.emit(stuff)`
    # Happens asynchronously on a separate thread to keep the ui fast
    def refresh(self):
        pass

    # Subclasses implement to update text labels, draw graphs, etc.
    # Happens on the main thread
    def set_content(self, content):
        pass
