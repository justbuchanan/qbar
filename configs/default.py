# Default configuration for qbar. Intended to be a good starting point, but easy
# to customize. Disable items by removing them from the list. Add new items by
# browsing with $python3 -c 'import qbar.items; help(qbar.items)' or by writing
# your own.

from qbar.items import *
from qbar.font_awesome import *

items = [
    MonitorNameBarItem(),
    BspwmBarItem(),
    SpacerBarItem(),
    WindowTitleBarItem(),
    SpacerBarItem(),
    AlsaVolumeBarItem(),
    WifiBarItem(interface="wlp2s0"),
    BatteryBarItem(),
    DateTimeBarItem(icon=FA_CALENDAR, format="%a %b %d"),   # date
    DateTimeBarItem(icon=FA_CLOCK_O, format="%H:%M"),       # time
]
