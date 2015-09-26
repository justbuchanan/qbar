from qbar.items.simple_bar_item import SimpleBarItem
import subprocess
from threading import Thread


class WindowTitleBarItem(SimpleBarItem):
    def __init__(self):
        super().__init__(text="<Window Title>")

        self._proc = subprocess.Popen(['xtitle', '-s'], stdout=subprocess.PIPE)

        Thread(target=self.run).start()

    def run(self):
        for line in self._proc.stdout:
            self.text = line.rstrip().decode('utf-8')
