from qbar.items.simple_bar_item import *
from qbar.font_awesome import *
from qbar.bspwm_status import *

import subprocess
from threading import Thread


class DesktopTitleBarItem(SimpleBarItem):
    def __init__(self, icon=FA_DESKTOP, monitor_index=0):
        super().__init__(icon, "monitor %d" % monitor_index)
        self._monitor_index = monitor_index
        self._proc = subprocess.Popen(['bspc', 'control', '--subscribe'], stdout=subprocess.PIPE)
        Thread(target=self.run).start()


    def run(self):
        for line in self._proc.stdout:
            wm_info = parse_bspwm_status(line.rstrip().decode('utf-8'))
            monitor = wm_info[self.monitor_index]

            # find focused desktop index and set text to its name
            desktop_index = -1
            for i in range(len(monitor.desktops)):
                d = monitor.desktops[i]
                if d.state in [Desktop.State.FocusedOccupied, Desktop.State.FocusedFree, Desktop.State.FocusedUrgent]:
                    # desktop_index = i
                    self.text = d.name
                    break

    @property
    def monitor_index(self):
        return self._monitor_index
