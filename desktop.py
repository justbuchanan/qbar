#!/usr/bin/env python3

import os
import sys
import subprocess
import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from qbar.font_awesome import *

app = QApplication([])
desktop = QApplication.desktop()


mon_names = [screen.name() for screen in app.screens()]
logging.debug("monitor names: %s" % ", ".join(mon_names))

# TODO: do intelligent info with these things
app.screenAdded.connect(lambda screen: print("Screen added: %s" % str(screen)))
app.screenRemoved.connect(lambda screen: print("Screen removed: %s" % str(screen)))
app.applicationStateChanged.connect(lambda state: print("Desktop app state changed: %s" % str(state)))


# Set the number and name of desktops in each monitor
desktop_names = {
    "DP1": [
        'robocup'
    ],
    "eDP1": [
        "web", "chat", "sys"
    ]
}
for monitor_name, desktops in desktop_names.items():
    os.system("bspc monitor %s -d %s" % (monitor_name, " ".join(["\"%s\"" % d for d in desktops])))


# config values
top_bar_height = 30
bottom_bar_height = 30

def bspc_cfg(var, val):
    os.system("bspc config %s %s" % (str(var), str(val)))

bars = []
for i in range(desktop.screenCount()):
    logging.info("Launching bars for monitor '%d'" % i)
    # Load up top bars, using a different config for the main screen vs extras
    args = ['python3', '-m', 'qbar.main', "--screen=%d" % i]
    top_cfg = 'qbar-default.yml' if i == desktop.primaryScreen() else 'nonmain-top.yml'
    bottom_cfg = 'bottom.yml' if i == desktop.primaryScreen() else 'nonmain-bottom.yml'
    bars.append({
        'top': subprocess.Popen(args + ['--config=%s' % top_cfg, '--height=%d' % top_bar_height]),
        'bottom': subprocess.Popen(args + ['--config=%s' % bottom_cfg, '--bottom=True', '--height=%d' % bottom_bar_height]),
    })

# Layout
logging.info("Applying bar-sized insets to bspwm's usable space")
bspc_cfg('top_padding', top_bar_height)
bspc_cfg('bottom_padding', bottom_bar_height)

# Define but don't call a method for exiting the program
def kill():
    # kill subprocesses before exiting
    for screen in bars:
        for pos in ['top', 'bottom']:
            screen[pos].terminate()

    # wait for them to exit
    for screen in bars:
        for pos in ['top', 'bottom']:
            screen[pos].wait()

    logging.info("Un-applying bar-sized wm insets...")
    bspc_cfg('top_padding', 0)
    bspc_cfg('bottom_padding', 0)

# Exit if user hits Ctrl+C We launch a timer that does nothing so that the
# python interpreter runs often enough to catch ctrl+c events.  See this
# stackoverflow for more info: http://stackoverflow.com/questions/4938723/what-
# is-the-correct-way-to-make-my-pyqt-application-quit-when-killed-from-the-co
sigtimer = QTimer()
sigtimer.timeout.connect(lambda: None)
sigtimer.start(500)
import signal
def signal_handler(signal, frame):
    print("Received Ctrl+C, exiting...")
    kill()
    app.exit(0)
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit')

ret = app.exec_()
sys.exit(ret)
