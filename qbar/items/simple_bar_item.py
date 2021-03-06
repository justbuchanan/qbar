from qbar.bar_item import BarItem
from qbar.font_awesome import *
from PyQt5.QtWidgets import QHBoxLayout, QLabel


# Shows an image and a piece of text side-by-side
class SimpleBarItem(BarItem):
    def __init__(self, icon=None, text=""):
        super().__init__()
        self._text_widget = QLabel(text)
        layout = QHBoxLayout()
        layout.addWidget(self._text_widget)
        layout.setContentsMargins(0,0,0,0)
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
        # Delete old icon if present
        if self._icon != None:
            self._icon.setParent(None)

        # If the user passed a string, make a FontAwesomeIcon out of it
        self._icon = FontAwesomeIcon(value) if isinstance(value, str) else value

        if self._icon != None:
            self.layout().insertWidget(0, self._icon)
