from qbar.items.periodic_bar_item import PeriodicBarItem
from qbar.font_awesome import *
import wifi
import re


class WifiBarItem(PeriodicBarItem):
    def __init__(self, interface, icon=FA_SIGNAL_WIFI_OFF, interval=2):
        super().__init__(icon=icon, text="WiFi", interval=interval)
        self._interface = interface

    def refresh(self):
        try:
            connections = list(wifi.scan.Cell.all(self.interface))
        except wifi.exceptions.InterfaceError as e:
            connections = []

        self.content_changed.emit(connections)

    def set_content(self, connections):
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
