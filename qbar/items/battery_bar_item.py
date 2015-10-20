from qbar.items.periodic_bar_item import PeriodicBarItem
from qbar.font_awesome import *
import power
import os


class BatteryBarItem(PeriodicBarItem):
    ## @param supply_name The filename under /sys/class/ for the battery we're
    #  interested in
    def __init__(self, icon=FA_BATTERY_FULL, supply_name='BAT0', interval=2):
        super().__init__(icon, "Battery", interval)
        self._supply_name = supply_name

    @property
    def supply_name(self):
        return self._supply_name
    
    def refresh(self):
        power_type = power.PowerManagement().get_providing_power_source_type()
        charging = (power_type == power.POWER_TYPE_AC)

        # supply_path = os.path.join("/sys/class/power_supply", self.supply_name)
        # energy_full, energy_now, power_now = power.PowerManagement.get_battery_state(supply_path)
        # print("efull: %f, enow: %f, pownow: %f", energy_full, energy_now, power_now)

        percent = 100 # TODO

        self.content_changed.emit((charging, percent))


    def set_content(self, info):
        charging, percent = info
        self.icon = FA_PLUG if charging else FA_BATTERY_FULL
        self.text = "%d%%" % percent
