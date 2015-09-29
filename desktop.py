#!/usr/bin/env python3

import os
import sys
import subprocess as sp
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# app = QGuiApplication([])
# print("started app")
app = QApplication([])
desktop = QApplication.desktop()


# for screen in app.screens():
#     print("desktop name: %s" % str(screen.name))

# TODO: do intelligent info with these things
# app.screenAdded.connect(lambda screen: "Screen added: %s" % str(screen))
# app.screenRemoved.connect(lambda screen: "Screen removed: %s" % str(screen))


# for i in range(desktop.screenCount()):
#     print("desktop name: %s" % str(desktop.screen(i)))


desktop_names = {
    "DP1": [
        "jb", "src", "rc"
    ],
    "eDP1": [
        "web", "chat", "sys"
    ]
}
for monitor_name, desktops in desktop_names.items():
    os.system("bspc monitor %s -d %s" % (monitor_name, " ".join(["\"%s\"" % d for d in desktops])))


bars = []

# config values
top_bar_height = 30
bottom_bar_height = 30

def bspc_cfg(var, val):
    os.system("bspc config %s %s" % (str(var), str(val)))

for i in range(desktop.screenCount()):
    print("Launching bars for monitor '%d'" % i)
    # Load up top bars, using a different config for the main screen vs extras
    args = ['python3', '-m', 'qbar.main', "--screen=%d" % i]
    top_cfg = 'qbar-default.yml' if i == desktop.primaryScreen() else 'nonmain-top.yml'
    bottom_cfg = 'bottom.yml' if i == desktop.primaryScreen() else 'nonmain-bottom.yml'
    bars.append({
        'top': sp.Popen(args + ['--config=%s' % top_cfg, '--height=%d' % top_bar_height]),
        'bottom': sp.Popen(args + ['--config=%s' % bottom_cfg, '--bottom=True', '--height=%d' % bottom_bar_height]),
    })

# Layout
print("Applying bar-sized insets to bspwm's usable space")
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

    print("Un-applying bar-sized wm insets...")
    bspc_cfg('top_padding', 0)
    bspc_cfg('bottom_padding', 0)

# Exit if user hits Ctrl+C
import signal
def signal_handler(signal, frame):
    print("Received Ctrl+C, exiting...")
    kill()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit')
signal.pause()
