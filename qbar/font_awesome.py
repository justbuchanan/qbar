from PyQt5.QtWidgets import QLabel

# A few selected icon character codes
FA_WIFI="\uf1eb"
FA_SIGNAL_WIFI_OFF="\ue1da"
FA_BATTERY_FULL="\uf240"
FA_CLOCK_O="\uf017"



class FontAwesomeIcon(QLabel):
    def __init__(self, code):
        super().__init__(code)
        self.setStyleSheet("font: FontAwesome");

    def cssClass(self):
        return QString("FontAwesomeIcon");
