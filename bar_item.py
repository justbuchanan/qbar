from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout





class BarItem(QWidget):
    pass


# class SpacerBarItem(QWidget):
#     pass


class FontAwesomeIcon(QLabel):
    def __init__(self, code):
        super().__init__(code)

    def cssClass(self):
        return QString("FontAwesomeIcon");


# Shows an image and a piece of text side-by-side
class SimpleBarItem(QWidget):
    def __init__(self, icon=None, text=""):
        super().__init__()
        self._text_widget = QLabel(text)
        layout = QHBoxLayout()
        layout.addWidget(self._text_widget)
        self.setLayout(layout)

        self._icon = None
        self.icon = icon

    @property
    def text(self):
        return self._text_widget.text()
    @text.setter
    def text(self, value):
        self._text_widget.setText(value)

    @property
    def text_widget(self):
        return self._text_widget
    

    ## @icon is a QWidget - could be a label using FontAwesome or an image widget
    @property
    def icon(self):
        return self._icon
    @icon.setter
    def icon(self, value):
        if self._icon != None:
            self.layout().takeAt(0)
        self._icon = value
        if self._icon != None:
            self.layout().insertWidget(0, self._icon)



FA_WIFI="\uf1eb"
FA_SIGNAL_WIFI_OFF="\ue1da"
FA_BATTERY_FULL="\uf240"


# A SimpleBarItem that periodically updates its content
from PyQt5.QtCore import QTimer
class PeriodicBarItem(SimpleBarItem):
    ## @interval is in seconds (may be partial)
    def __init__(self, icon=None, text="", interval=2):
        super().__init__(icon, text)
        self._timer = QTimer(self)
        self._timer.setInterval(interval * 1000) # convert to ms
        self._timer.timeout.connect(self.refresh)
        self._timer.start()

    def refresh(self):
        pass



import wifi
import re
class WifiBarItem(PeriodicBarItem):
    def __init__(self, interface, interval=2):
        super().__init__(FontAwesomeIcon(FA_SIGNAL_WIFI_OFF), "WiFi", interval)
        self._interface = interface


    def refresh(self):
        try:
            connections = list(wifi.scan.Cell.all(self.interface))
        except wifi.exceptions.InterfaceError as e:
            connections = []

        if len(connections) == 0:
            self.icon = FontAwesomeIcon(FA_SIGNAL_WIFI_OFF)
            self.text = "No WiFi"
        elif len(connections) == 1:
            self.icon = FontAwesomeIcon(FA_WIFI)
            # qual_str = connections[0].quality
            # vals = re.match(r"^(\d+)/(\d+)", qual_str).groups()
            # percent = int(float(vals[0]) / float(vals[1]) * 100)
            # self.text = "%d%%" % percent
            self.text = connections[0].ssid
        else:
            self.icon = FontAwesomeIcon(FA_SIGNAL_WIFI_OFF)
            self.text = "Scanning..."


    @property
    def interface(self):
        return self._interface


import power


class BatteryBarItem(PeriodicBarItem):
    def __init__(self, interval=2):
        super().__init__(FontAwesomeIcon(FA_BATTERY_FULL), "Battery", interval)

    def refresh(self):
        # man = power.PowerManagement.is_battery_present()
        self.text = "100%"
        # TODO: figure out how to use the power module



FA_CLOCK_O="\uf017"

import time
class DateTimeBarItem(PeriodicBarItem):
    def __init__(self, format="%H:%M %a", interval=2):
        super().__init__(FontAwesomeIcon(FA_CLOCK_O), "Time", interval)
        self._format = format

    def refresh(self):
        self.text = time.strftime(self.format)

    @property
    def format(self):
        return self._format
    