#!/usr/bin/env python3

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget
import logging
import argparse
import signal
import sys

from bar import Bar
from bar_item import *


# Exit app on ctrl+c
def sigint_handler(signal, frame):
    print("handler")
    QApplication.quit()
signal.signal(signal.SIGINT, sigint_handler)


# Command-line arguments
parser = argparse.ArgumentParser(description="A minimalist and easy-to-use status bar using Qt")
parser.add_argument(
    "--screen_index",
    type=int,
    default=-1,
    help="Index of the screen to display the bar")
parser.add_argument(
    "--height",
    type=int,
    default=30,
    help="Height (in px) of the status bar")
parser.add_argument(
    "--css",
    type=str,
    default=None,
    help="Stylesheet file to override the default style")
ARGS = parser.parse_args()


# Init app
app = QApplication(sys.argv)

# Init bar
bar = Bar([BatteryBarItem(), WifiBarItem("wlp2s0"), DateTimeBarItem()])

# Bar geometry
desktop = QApplication.desktop()
x = 0
for i in range(0, ARGS.screen_index):
    x += desktop.screenGeometry(ARGS.screen_index).width()
geom = desktop.screenGeometry(ARGS.screen_index)
bar.setGeometry(x, 0, geom.width(), ARGS.height)


# Set default stylesheet and override with custom one if present
styles = ""
with open("qbar-default.css") as stylefile:
    styles = stylefile.read()
if ARGS.css != None:
    with open(ARGS.css) as stylefile_custom:
        styles += "\n" + stylefile_custom.read()
    logging.info("Loaded custom stylesheet: '%s'", ARGS.css)
app.setStyleSheet(styles)

# Run!
bar.show()
sys.exit(app.exec_())
