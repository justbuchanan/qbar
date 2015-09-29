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
import qbar.items as items_module


# Returns list of BarItem objects as specified in the config file
def load_items_from_config(filepath):
    # Get a list of the names of the modules containing BarItem subclasses
    items_path = os.path.dirname(__file__) + "/items"
    item_modules = [tup[1] for tup in pkgutil.iter_modules([items_path])]
    for module_name in item_modules:
        importlib.import_module("qbar.items.%s" % module_name)


    # Load config file
    try:
        with open(filepath, 'r') as cfgfile:
            cfg = yaml.load(cfgfile)
    except FileNotFoundError as e:
        # If the user-specified pat
        # logging.warn("Unable to find user config file, using builtin fallback")
        fallback_cfgfile_path = os.path.abspath(os.path.dirname(__file__)) + "/../configs/qbar-default.yml"
        with open(fallback_cfgfile_path, 'r') as cfgfile:
            cfg = yaml.load(cfgfile)

    items = []
    for item_info in cfg['items']:
        class_name = item_info['type'] + "BarItem"
        logging.info("Loading item of type: '%s'" % item_info['type'])

        klass = None
        for module_name in item_modules:
            try:
                mod = getattr(items_module, module_name)
                klass = getattr(mod, class_name)
                break
            except AttributeError as e:
                klass = None
        if klass == None:
            logging.error("Unable to find BarItem of type '%s', ignoring..." % item_info['type'])
            continue

        kwargs = dict(item_info)
        kwargs.pop('type', None)
        items += [klass(**kwargs)]

    return items


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

    def reload_config(filepath):
        bar.items = load_items_from_config(filepath)

    # Load config file and set it up to reload whenever the file changes
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
