from qbar.items import *
from qbar.font_awesome import *

items = [
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
