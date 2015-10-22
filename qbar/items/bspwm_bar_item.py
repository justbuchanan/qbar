from qbar.items.simple_bar_item import *
from qbar.bar_item import *
from qbar.font_awesome import *
from qbar.bspwm_status import *

from PyQt5.QtCore import pyqtSignal
from subprocess import check_output, Popen, PIPE
from threading import Thread
import math


class DesktopItem(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
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
        p.setRenderHint(QPainter.Antialiasing)

        # Use foreground color for underline and "window dots"
        styleOpt = QStyleOption()
        styleOpt.initFrom(self)
        gcolor = styleOpt.palette.color(QPalette.Text)
        p.setBrush(gcolor)
        p.setPen(gcolor)

        # draw an underline if thid desktop is currently focused
        focused_states = [
            Desktop.State.FocusedOccupied,
            Desktop.State.FocusedFree,
            Desktop.State.FocusedUrgent
        ]
        if self._desktop_info.state in focused_states:
            thickness = 1
            rect = self.rect()
            p.drawRect(0, rect.height() - thickness, rect.width(), thickness)

        # draw dots centered above the name to indicate the number of open windows
        spacing = 3
        rad = 3
        totalw = (self._desktop_info.num_windows * (spacing + rad)) - spacing
        startx = (self.rect().width() - totalw) / 2
        y = 3
        for i in range(self._desktop_info.num_windows):
            bbox = QRectF(startx + i*(spacing + rad), y, rad, rad)
            p.drawEllipse(bbox)

        # Vertical line border
        if False:
            rect = self.rect()
            inset = 10
            w = 0.02
            r = QRectF(rect.width() - w, inset, w, rect.height() - inset*2)
            p.drawRect(r)



class BspwmBarItem(BarItem):

    # Use a signal to pass content from the processing thread to the main UI thread
    info_changed = pyqtSignal(list)


    def __init__(self):
        super().__init__()
        self._proc = None
        self._thread = None

        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        self._desktop_widgets = []
        self._monitor_info = None
        self.info_changed.connect(self.set_info)


    def start(self):
        if self._proc == None:
            self._proc = Popen(['bspc', 'control', '--subscribe'], stdout=PIPE)
            self._thread = Thread(target=self.run)
            self._thread.start()

    def stop(self):
        if self._proc != None:
            self._proc.terminate()
            self._proc.wait()
            self._thread.join()
            self._proc = None
            self._thread = None

    def run(self):
        for line in self._proc.stdout:
            wm_info = parse_bspwm_status(line.rstrip().decode('utf-8'))
            self.info_changed.emit(wm_info)


    def set_info(self, info):
        self._monitor_info = None
        for monitor_info in info:
            if self.bar != None and monitor_info.name == self.bar.monitor_name:
                self._monitor_info = monitor_info
                break

        if self._monitor_info == None:
            # TODO: handle this
            return

        # Add or remove DesktopItem objects to match the number of desktops
        # specified in the info
        diff = len(self._monitor_info.desktops) - len(self._desktop_widgets)
        while diff > 0:
            diff -= 1
            d = DesktopItem()
            self.layout().addWidget(d)
            self._desktop_widgets.append(d)
        while diff < 0:
            diff += 1
            self._desktop_widgets.pop(0)
            w = self.layout().takeAt(0).widget()
            if w != None:
                w.setParent(None)

        # Update the info for each DesktopItem widget
        for i in range(len(self._monitor_info.desktops)):
            desktop = self._monitor_info.desktops[i]
            widget = self._desktop_widgets[i]
            # get a window count for this desktop
            out = check_output(['bspc', 'query', '-W', '-d', "%s:^%d" % (self._monitor_info.name, i+1)]).decode('utf-8').strip().split('\n')
            out = [w for w in out if w != '']
            num = len(out)
            desktop.num_windows = num

            widget.set_info(desktop)
