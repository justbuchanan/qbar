from qbar.items.simple_bar_item import *
from qbar.font_awesome import *
from qbar.bspwm_status import *

import subprocess
from threading import Thread


class WeatherBarItem(SimpleBarItem):
    def __init__(self, icon=FA_CLOUD, monitor_index=0):
        super().__init__(icon, "75°F - ATL")
