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

from qbar import *
from qbar.bar import Bar
from qbar.stylesheet_loader import StyleSheetLoader
from qbar.bar_item import *


# Returns list of BarItem objects as specified in the config file
def load_config_module(filepath):
    sys.path.insert(0, os.path.dirname(filepath))
    cfg_module = importlib.import_module(os.path.basename(os.path.splitext(filepath)[0]))
    return cfg_module


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
        "--monitor",
        "-m",
        type=str,
        default=None,
        help="Name of the monitor to display the bar on")

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
        "--log-level",
        "-l",
        default='WARNING',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help="Change the level of information to be logged.")
    ARGS = parser.parse_args()

    # Log level for the root logger
    numeric_log_level = getattr(logging, ARGS.log_level.upper(), None)
    logging.getLogger().setLevel(numeric_log_level)

    # Init app
    app = QApplication(sys.argv)
    bar = Bar(ARGS.monitor, height=ARGS.height, position=ARGS.position)

    # Set default stylesheet and override with custom one if present
    stylesheet_files = [os.path.abspath(os.path.dirname(__file__)) + "/../configs/default.css"]
    if ARGS.css != None:
        stylesheet_files.append(ARGS.css)
    css_loader = StyleSheetLoader(stylesheet_files, lambda styles: app.setStyleSheet(styles))

    # Find config file path
    cfgfile = ARGS.config if ARGS.config != None else default_user_config_dir() + '/config.py'
    if not os.path.exists(cfgfile):
        if ARGS.config != None:
            logging.error("Specified config file does not exist: %s" % ARGS.config)
        logging.info("Using builtin default config file")
        cfgfile = os.path.abspath(os.path.dirname(__file__)) + "/../configs/default.py"

    # Load config file and set it up to reload whenever the file changes
    cfgmodule = load_config_module(cfgfile)
    bar.items = cfgmodule.items
    def reload_config(filepath):
        logging.info("Config file changed, reloading: %s" % filepath)
        try:
            importlib.reload(cfgmodule)
            bar.items = cfgmodule.items
        except SyntaxError as e:
            logging.error("SyntaxError encountered when attempting to load config file: %s" % str(e))
            bar.items = []
    watcher = QFileSystemWatcher()
    watcher.addPath(cfgfile)
    watcher.fileChanged.connect(reload_config)

    # Run!
    bar.start()
    bar.show()

    # Exit app on ctrl+c.
    # Note that a timer must be present in order for Ctrl+C to work. Otherwise
    # the python interpreter never gets a chance to run and handle the signal.
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
