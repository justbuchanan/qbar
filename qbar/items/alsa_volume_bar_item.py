from qbar.items.periodic_bar_item import PeriodicBarItem
from qbar.font_awesome import *
import alsaaudio


class AlsaVolumeBarItem(PeriodicBarItem):
    def __init__(self, interval=0.5):
        super().__init__(FA_VOLUME_UP, "Volume")

    def refresh(self):
        mixer = alsaaudio.Mixer()
        volume_percent = mixer.getvolume()[0]
        if volume_percent > 50:
            self.icon = FA_VOLUME_UP
        elif volume_percent == 0:
            self.icon = FA_VOLUME_OFF
        else:
            self.icon = FA_VOLUME_DOWN
        self.text = "%d%%" % volume_percent
