from os.path import dirname, basename, isfile
from importlib import import_module
import glob
import sys

# Import all contents of the modules in this subdirectory so they can be
# accessed externally with: `from qbar.items import *`
sys.path.insert(0, dirname(__file__))
mod_paths = glob.glob(dirname(__file__) + "/*.py")
for filename in mod_paths:
    modname = basename(filename)[:-3]
    if modname == '__init__': continue
    mod = import_module(modname)
    for attr in dir(mod):
        if not attr.startswith('_'):
            globals()[attr] = getattr(mod, attr)
del sys.path[0]
