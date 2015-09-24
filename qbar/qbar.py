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
    print("\nReceived ctrl+c, exiting...")
    QApplication.quit()
signal.signal(signal.SIGINT, sigint_handler)


# Command-line arguments
parser = argparse.ArgumentParser(description="A minimalist and easy-to-use status bar using Qt")
parser.add_argument(
    "--screen",
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
parser.add_argument(
    "--config",
    "-c",
    default="~/.config/qbar.yml",
    help="Congifuration file for qbar written in yaml")
ARGS = parser.parse_args()

# logging.basicConfig(level=logging.INFO)


# Init app
app = QApplication(sys.argv)

# Set default stylesheet and override with custom one if present
styles = ""
with open("qbar-default.css", 'r') as stylefile:
    styles = stylefile.read()
if ARGS.css != None:
    with open(ARGS.css, 'r') as stylefile_custom:
        styles += "\n" + stylefile_custom.read()
    logging.info("Loaded custom stylesheet: '%s'", ARGS.css)
app.setStyleSheet(styles)



# Load config file
import yaml
with open("qbar-config.yml", 'r') as cfgfile:
    cfg = yaml.load(cfgfile)
items = []
for item_info in cfg:
    class_name = item_info['type'] + "BarItem"
    logging.info("Loading item of type: '%s'" % item_info['type'])
    klass = getattr(sys.modules[__name__], class_name)
    kwargs = dict(item_info)
    kwargs.pop('type', None)
    items += [klass(**kwargs)]


# Init bar
bar = Bar(items)

# Bar geometry
desktop = QApplication.desktop()
x = 0
for i in range(0, ARGS.screen):
    x += desktop.screenGeometry(ARGS.screen).width()
geom = desktop.screenGeometry(ARGS.screen)
bar.setGeometry(x, 0, geom.width(), ARGS.height)


# Run!
bar.show()
sys.exit(app.exec_())
