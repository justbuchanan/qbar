from qbar.items.periodic_bar_item import PeriodicBarItem
from qbar.font_awesome import *
import power


class BatteryBarItem(PeriodicBarItem):
    def __init__(self, interval=2):
        super().__init__(FontAwesomeIcon(FA_BATTERY_FULL), "Battery", interval)

    def refresh(self):
        # man = power.PowerManagement.is_battery_present()
        self.text = "100%"
        # TODO: figure out how to use the power module
