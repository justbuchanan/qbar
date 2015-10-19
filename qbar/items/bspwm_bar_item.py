from qbar.items.simple_bar_item import *
from qbar.bar_item import *
from qbar.font_awesome import *
from qbar.bspwm_status import *

import subprocess
from threading import Thread


class DesktopItem(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        # self.setSizeConstraint(QLayout.SetMaximumSize)

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self._desktop_info = None


    def set_info(self, desktop_info):
        self._desktop_info = desktop_info
        if self._desktop_info != None:
            self.setText(self._desktop_info.name)
        self.update()


    def paintEvent(self, event):



        super().paintEvent(event)


        p = QPainter(self)

        repr_by_state = {
            Desktop.State.FocusedOccupied: '■',
            Desktop.State.FocusedFree: '■',
            Desktop.State.FocusedUrgent: '■',
            Desktop.State.Occupied: '▪',
            Desktop.State.Free: '▫',
            Desktop.State.Urgent: '▪'
        }


        focused_states = [Desktop.State.FocusedOccupied, Desktop.State.FocusedFree, Desktop.State.FocusedUrgent]


        # Use foreground color for underline
        styleOpt = QStyleOption()
        styleOpt.initFrom(self)
        gcolor = styleOpt.palette.color(QPalette.Text)
        p.setBrush(gcolor)
        p.setPen(gcolor)

        if self._desktop_info.state in focused_states:
            h = 2
            rect = self.rect()
            p.drawRect(0, rect.height() - h, rect.width(), h)




class BspwmBarItem(BarItem):
    def __init__(self, icon=None, monitor_index=0):
        # super().__init__(icon, "monitor %d" % monitor_index)
        super().__init__()
        self._monitor_index = monitor_index

        self._proc = subprocess.Popen(['bspc', 'control', '--subscribe'], stdout=subprocess.PIPE)

        Thread(target=self.run).start()

        layout = QHBoxLayout()
        inset = 1
        layout.setContentsMargins(inset,0,inset,0)
        # print(layout.contentsMargins().top())
        # self.spacing = 15
        # layout.setSpacing(self.spacing)
        self.setLayout(layout)
        self._desktop_widgets = []

        self._monitor_info = None


    def run(self):
        for line in self._proc.stdout:
            # print(self.layout().contentsMargins().top())
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

            wm_info = parse_bspwm_status(line.rstrip().decode('utf-8'))
            self._monitor_info = wm_info[self.monitor_index]
            self.update()


    def paintEvent(self, event):
        super().paintEvent(event)

        # repr_by_state = {
        #     Desktop.State.FocusedOccupied: '●',
        #     Desktop.State.FocusedFree: '●',
        #     Desktop.State.FocusedUrgent: '●',
        #     Desktop.State.Occupied: '◉',
        #     Desktop.State.Free: '○',
        #     Desktop.State.Urgent: '●'
        # }

        if self._monitor_info == None:
            return
        #     # TODO
        #     return
        # print("mon: %s" % str(self._monitor_info))

        repr_by_state = {
            Desktop.State.FocusedOccupied: '■',
            Desktop.State.FocusedFree: '■',
            Desktop.State.FocusedUrgent: '■',
            Desktop.State.Occupied: '▪',
            Desktop.State.Free: '▫',
            Desktop.State.Urgent: '▪'
        }

        diff = len(self._monitor_info.desktops) - len(self._desktop_widgets)
        while diff > 0:
            diff -= 1

            d = DesktopItem()
            self.layout().addWidget(d)
            self._desktop_widgets.append(d)

        while diff < 0:
            diff += 1

            # self.layout().addWidget(d)
            # self._desktop_widgets.append(d)
            self._desktop_widgets.pop(0)
            w = self.layout().takeAt(0).widget()
            if w != None:
                w.setParent(None)


        for desktop, widget in zip(self._monitor_info.desktops, self._desktop_widgets):
            widget.set_info(desktop)





        # def desktop_text(d):
        #     return repr_by_state[d.state] + ' ' + d.name

        # self.text = " " + "   ".join([desktop_text(d) for d in self._monitor_info.desktops])
        # self.text.setFontUnderline()


    @property
    def monitor_index(self):
        return self._monitor_index
