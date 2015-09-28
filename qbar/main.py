from PyQt5 import QtWidgets, QtCore
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
from qbar.bar_item import *
import qbar.items as items_module


def main():
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
        default="~/.config/qbar.yml",
        help="Congifuration file for qbar written in yaml")
    ARGS = parser.parse_args()

    # logging.basicConfig(level=logging.INFO)


    # Init app
    app = QApplication(sys.argv)

    # Set default stylesheet and override with custom one if present
    styles = ""
    # TODO: what if file doesn't exist?  FileNotFouondError
    builtin_stylefile = os.path.abspath(os.path.dirname(__file__)) + "/../qbar-default.css"
    with open(builtin_stylefile, 'r') as stylefile:
        styles = stylefile.read()
    if ARGS.css != None:
        with open(ARGS.css, 'r') as stylefile_custom:
            styles += "\n" + stylefile_custom.read()
        logging.info("Loaded custom stylesheet: '%s'", ARGS.css)
    app.setStyleSheet(styles)


    # Get a list of the names of the modules containing BarItem subclasses
    items_path = os.path.dirname(__file__) + "/items"
    item_modules = [tup[1] for tup in pkgutil.iter_modules([items_path])]
    for module_name in item_modules:
        importlib.import_module("qbar.items.%s" % module_name)


    # Load config file
    try:
        with open(ARGS.config, 'r') as cfgfile:
            cfg = yaml.load(cfgfile)
    except FileNotFoundError as e:
        # If the user-specified pat
        logging.warn("Unable to find user config file, using builtin fallback")
        fallback_cfgfile_path = os.path.abspath(os.path.dirname(__file__)) + "/../qbar-default.yml"
        with open(fallback_cfgfile_path, 'r') as cfgfile:
            cfg = yaml.load(cfgfile)

    

    items = []
    for item_info in cfg['items']:
        # print("item_info: %s" % item_info)
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
    bar.start()
    bar.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
