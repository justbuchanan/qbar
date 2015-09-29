from PyQt5.QtWidgets import QLabel

# A few selected icon character codes for Font Awesome
FA_BATTERY_FULL="\uf240"
FA_CALENDAR="\uf073"
FA_CIRCLE="\uf111"
FA_CIRCLE_O="\uf10c"
FA_CLOCK_O="\uf017"
FA_CLOUD="\uf0c2"
FA_CODE="\uf121"
FA_DESKTOP="\uf108"
FA_PLUG="\uf1e6"
FA_POWER_OFF="\uf011"
FA_SIGNAL_WIFI_OFF="\ue1da"
FA_VOLUME_DOWN="\uf027"
FA_VOLUME_OFF="\uf026"
FA_VOLUME_UP="\uf028"
FA_WIFI="\uf1eb"

# A few selected icon codes for Google Material Design
MD_MUSIC_NOTE="\ue405"
MD_NETWORK_WIFI="\ue1ba"
MD_NETWORK_WIFI_OFF="\ue1da"
MD_RADIO_BUTTON_CHECKED="\ue837"
MD_STORAGE="\ue1db"
MD_TRENDING_UP="\ue8e5"
MD_TUNE="\ue429"
MD_VIEW_COMPACT="\ue42b"
MD_VIEW_QUILT="\ue8f1"
MD_VOLUME_OFF="\ue04f"
MD_BATTERY_FULL="\ue1a4"

class FontAwesomeIcon(QLabel):
    def __init__(self, code):
        super().__init__(code)
        self.setStyleSheet("font: FontAwesome")


class MaterialDesignIcon(QLabel):
    def __init__(self, code):
        super().__init__(code)
        self.setStyleSheet("font: MaterialIcons-Regular")
