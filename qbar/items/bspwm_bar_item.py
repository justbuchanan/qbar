from qbar.items.simple_bar_item import *
from qbar.font_awesome import *
from qbar.bspwm_status import *

import subprocess
from threading import Thread


class BspwmBarItem(SimpleBarItem):
    def __init__(self, icon=None, monitor_index=0):
        super().__init__(icon, "monitor %d" % monitor_index)
        self._monitor_index = monitor_index

        self._proc = subprocess.Popen(['bspc', 'control', '--subscribe'], stdout=subprocess.PIPE)

        Thread(target=self.run).start()


    def run(self):
        for line in self._proc.stdout:
            # repr_by_state = {
            #     Desktop.State.FocusedOccupied: '<font color=#6abed8>■</font>',
            #     Desktop.State.FocusedFree: '<font color=#6abed8>■</font>',
            #     Desktop.State.FocusedUrgent: '<font color=#6abed8>■</font>',
            #     Desktop.State.Occupied: '▣',
            #     Desktop.State.Free: '□',
            #     Desktop.State.Urgent: '<font color="orange">■</font>'
            # }
            # repr_by_state = {
            #     Desktop.State.FocusedOccupied: '■',
            #     Desktop.State.FocusedFree: '■',
            #     Desktop.State.FocusedUrgent: '■',
            #     Desktop.State.Occupied: '▣',
            #     Desktop.State.Free: '□',
            #     Desktop.State.Urgent: '■'
            # # }
            # repr_by_state = {
            #     Desktop.State.FocusedOccupied: '■',
            #     Desktop.State.FocusedFree: '■',
            #     Desktop.State.FocusedUrgent: '■',
            #     Desktop.State.Occupied: '▪',
            #     Desktop.State.Free: '▫',
            #     Desktop.State.Urgent: '▪'
            # }

            repr_by_state = {
                Desktop.State.FocusedOccupied: '●',
                Desktop.State.FocusedFree: '●',
                Desktop.State.FocusedUrgent: '●',
                Desktop.State.Occupied: '◉',
                Desktop.State.Free: '○',
                Desktop.State.Urgent: '●'
            }



            wm_info = parse_bspwm_status(line.rstrip().decode('utf-8'))
            monitor = wm_info[self.monitor_index]
            
            self.text = " " + " ".join([repr_by_state[d.state] + d.name for d in monitor.desktops])


    @property
    def monitor_index(self):
        return self._monitor_index
