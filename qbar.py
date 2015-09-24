#!/usr/bin/env python3

import sys
import signal
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore



def sigint_handler(signal, frame):
    print("handler")
    QApplication.quit()
signal.signal(signal.SIGINT, sigint_handler)

app = QApplication(sys.argv)
w = QWidget()
w.setWindowFlags(QtCore.Qt.X11BypassWindowManagerHint)
w.setGeometry(0, 0, 1920, 5)
w.setStyleSheet('background-color: black; color: white')





layout = QtWidgets.QHBoxLayout()

hello = QtWidgets.QLabel("Hello")
layout.addWidget(hello)

layout.addStretch()


w.setLayout(layout)

w.show()

sys.exit(app.exec_())
