from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QFileSystemWatcher, QTimer
from PyQt5.QtWidgets import QApplication, QWidget
import argparse
import importlib
import logging
import os
import pkgutil
import signal
import sys
import yaml

from qbar import *
from qbar.bar import Bar
from qbar.stylesheet_loader import StyleSheetLoader
from qbar.bar_item import *


# Returns list of BarItem objects as specified in the config file
def load_items_from_config(filepath):
    # Use builtin fallback if no config is specified or if it doesn't exist
    if filepath == None or not os.path.isfile(filepath):
        filepath = os.path.abspath(os.path.dirname(__file__)) + "/../configs/default.py"

    sys.path.insert(0, os.path.dirname(filepath))
    cfg_module = importlib.import_module(os.path.basename(os.path.splitext(filepath)[0]))
    return cfg_module.items


def default_user_config_dir():
    dirname = 'qbar'
    if 'XDG_HOME' in os.environ:
        return os.path.join(os.environ['XDG_HOME'], dirname)
    else:
        return "~/.config/%s" % dirname


def main():
    # Command-line arguments
    parser = argparse.ArgumentParser(
        prog='qbar',
        description="An easily-configurable and good-looking status bar for Linux")
    parser.add_argument(
        "--screen",
        type=int,
        default=-1,
        help="Index of the screen to display the bar")

    # TODO: use css for this instead?
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
        default=None,
        help="Congifuration file for qbar written in yaml.  Looks under $XDG_HOME or .config for qbar/config.yml by default.  if not found, uses a builtin default")
    parser.add_argument(
        "--position",
        "-p",
        type=str,
        default="top",
        choices=["top", "bottom"],
        help="Display position of the bar.  Can be 'top' or 'bottom'")
    parser.add_argument(
        "--verbose",
        "-v",
        action='store_true',
        help="Log debug information as qbar runs")
    ARGS = parser.parse_args()

    # Optional verbose logging
    if ARGS.verbose:
        logging.setLevel(logging.DEBUG)

    # Init app
    app = QApplication(sys.argv)

    # Set default stylesheet and override with custom one if present
    stylesheet_files = [os.path.abspath(os.path.dirname(__file__)) + "/../configs/qbar-default.css"]
    if ARGS.css != None:
        stylesheet_files.append(ARGS.css)
    css_loader = StyleSheetLoader(stylesheet_files, lambda styles: app.setStyleSheet(styles))

    # create the bar
    bar = Bar()

    # Load config file and set it up to reload whenever the file changes
    def reload_config(filepath):
        bar.items = load_items_from_config(filepath)
    cfgfile = ARGS.config if ARGS.config != None else default_user_config_dir() + '/config.yml'
    watcher = QFileSystemWatcher()
    watcher.addPath(cfgfile)
    watcher.fileChanged.connect(reload_config)
    reload_config(cfgfile)
    
    # Bar geometry
    # Place it based on the "screen" and "bottom" config variables
    desktop = QApplication.desktop()
    x = 0
    geom = desktop.screenGeometry(ARGS.screen)
    for i in range(0, ARGS.screen):
        x += geom.width()
    y = geom.height() - ARGS.height if ARGS.position == "bottom" else 0
    bar.setGeometry(x, y, geom.width(), ARGS.height)

    # Run!
    bar.start()
    bar.show()

    # Exit app on ctrl+c
    # Note that a timer must be present in order for Ctrl+C to work. Otherwise the python interpreter never gets a chance to run and handle the signal.
    sigtimer = QTimer()
    sigtimer.timeout.connect(lambda: None)
    sigtimer.start(500)
    def sigint_handler(signal, frame):
        print("\nReceived Ctrl+C, exiting...")
        bar.stop()
        QApplication.quit()
    signal.signal(signal.SIGINT, sigint_handler)

    ret = app.exec_()
    sys.exit(ret)


if __name__ == '__main__':
    main()
