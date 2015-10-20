from qbar.items.periodic_bar_item import PeriodicBarItem
import psutil


class DiskIoBarItem(PeriodicBarItem):
    def __init__(self, icon="io", interval=0.5, datapoints=20):
        super().__init__(icon=icon, interval=interval)
        self._history = collections.deque(maxlen=datapoints)

    # Circular buffer of past disk i/o readings
    @property
    def history(self):
        return self._history

    def refresh(self):
        # io_info = psutil.disk_io_counters(perdisk=False)
        # write_count
        pass



