from qbar.items.simple_bar_item import SimpleBarItem
import subprocess
from threading import Thread
import shutil


# Displays the title of the currently-focused window (uses xtitle)
class WindowTitleBarItem(SimpleBarItem):
    def __init__(self, icon=None):
        super().__init__(icon=icon, text="<Window Title>")
        self._proc = None
        self._thread = None
        if shutil.which('xtitle') == None:
            raise RuntimeError("Can't use WindowTitleBarItem without having 'xtitle' installed")

    def start(self):
        super().start()
        if self._proc == None:
            self._proc = subprocess.Popen(['xtitle', '-s'], stdout=subprocess.PIPE)
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
            self.text = line.rstrip().decode('utf-8')
