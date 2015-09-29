from qbar.items.simple_bar_item import *
from qbar.font_awesome import *
from qbar.bspwm_status import *

import subprocess
from threading import Thread
import shutil


class DesktopTitleBarItem(SimpleBarItem):
    def __init__(self, icon=FA_DESKTOP, monitor_index=0):
        super().__init__(icon, text="<Desktop Title>")
        self._monitor_index = monitor_index
        self._proc = None
        self._thread = None
        if shutil.which('xtitle') == None:
            raise RuntimeError("Can't use DesktopTitleBarItem without having 'xtitle' installed")

    def start(self):
        super().start()
        if self._proc == None:
            self._proc = subprocess.Popen(['bspc', 'control', '--subscribe'], stdout=subprocess.PIPE)
            self._thread = Thread(target=self.run)
            self._thread.start()

    def stop(self):
        super().stop()
        if self._proc != None:
            self._proc.terminate()
            self._proc.wait()
            self._thread.join()
            self._proc = None
            self._thread = None

    def run(self):
        for line in self._proc.stdout:
            wm_info = parse_bspwm_status(line.rstrip().decode('utf-8'))
            monitor = wm_info[self.monitor_index]

            # find focused desktop index and set text to its name
            for i in range(len(monitor.desktops)):
                d = monitor.desktops[i]
                if d.state in [Desktop.State.FocusedOccupied, Desktop.State.FocusedFree, Desktop.State.FocusedUrgent]:
                    self.text = d.name
                    break

    @property
    def monitor_index(self):
        return self._monitor_index
