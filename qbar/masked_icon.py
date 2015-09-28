from PyQt5.QtGui import QPainter, QPainterPath, QPalette, QPixmap, QImage, QRegion, QBitmap
from PyQt5.QtCore import Qt, QPointF, QSize
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle, QLabel
from PyQt5 import QtCore

## An icon created by masking an image.  This allows its color to be set through the css "color" property for the widget
class MaskedImageIcon(QLabel):
    def __init__(self, iconfile):
        super().__init__()
        # TODO: on-the fly sizing
        # img = QImage(iconfile).scaled(QSize(30, 30))
        # print("img: " + str(img))
        # self._mask = QBitmap(QPixmap.fromImage(img.createAlphaMask()))

        img = QImage(iconfile).scaled(QSize(15, 15))
        # print("img: " + str(img))
        # self._mask = QBitmap(QPixmap.fromImage(img.createAlphaMask()))
        self.setPixmap(QBitmap(QPixmap.fromImage(img.createAlphaMask())))
        # self.resize(30, 30)
        # self.resize(30, 30)


