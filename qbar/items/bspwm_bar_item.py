from qbar.items.simple_bar_item import *
from qbar.bar_item import *
from qbar.font_awesome import *
from qbar.bspwm_status import *

import subprocess
from threading import Thread

from PyQt5.QtCore import pyqtSignal


# TODO: at init time, we need to query for first infos...


class DesktopItem(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

        self._desktop_info = None


    def set_info(self, desktop_info):
        print('info set')
        self._desktop_info = desktop_info
        if self._desktop_info != None:
            name = self._desktop_info.name
            d = 5 - len(name)
            if d < 0: d = 0
            name += " " * d
            self.setText(name)
        self.update()


    def paintEvent(self, event):
        super().paintEvent(event)

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

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


        spacing = 3
        w = 3
        for i in range(self._desktop_info.num_windows):
            print("desktop %s : %d" % (self._desktop_info.name, self._desktop_info.num_windows))
            r = QRectF(i*(spacing + w), 0, w, w)
            p.drawRect(r)

        # Vertical separators
        rect = self.rect()
        inset = 6
        w = 1
        r = QRectF(rect.width() - w, inset, w, rect.height() - inset*2)
        # p.drawRect(r)




class BspwmBarItem(BarItem):

    info_changed = pyqtSignal(list)


    def __init__(self, icon=None, monitor_index=0):
        # super().__init__(icon, "monitor %d" % monitor_index)
        super().__init__()
        self._monitor_index = monitor_index

        self._proc = subprocess.Popen(['bspc', 'control', '--subscribe'], stdout=subprocess.PIPE)

        Thread(target=self.run).start()

        layout = QHBoxLayout()
        inset = 1
        layout.setContentsMargins(inset,0,inset,0)
        self.setLayout(layout)
        self._desktop_widgets = []

        self._monitor_info = None

        self.info_changed.connect(self.set_info)


    def run(self):
        for line in self._proc.stdout:
            wm_info = parse_bspwm_status(line.rstrip().decode('utf-8'))
            self.info_changed.emit(wm_info)


    def set_info(self, info):
        self._monitor_info = info[self.monitor_index]

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
            from subprocess import check_output
            out = check_output(['bspc', 'query', '-W', '-d', desktop.name]).decode('utf-8').strip().split('\n')
            out = [w for w in out if w != '']
            num = len(out)
            desktop.num_windows = num

            widget.set_info(desktop)

        self.update()


    @property
    def monitor_index(self):
        return self._monitor_index
