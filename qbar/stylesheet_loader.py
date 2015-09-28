from PyQt5.QtCore import QFileSystemWatcher
import logging

## This class is used to load css files for use with the status bar.  Initialize
#  it with a list of filepaths and a callback function to be called whenever one
#  of the files changes.  This makes it easy to have the bar's style update
#  automatically whenever a relevant css file changes.
class StyleSheetLoader:
    ## @param filepaths A list of paths to css files with the highest-priority
    # file last
    def __init__(self, filepaths, callback):
        self._filepaths = filepaths
        self._fs_watcher = QFileSystemWatcher(self.filepaths)
        self._fs_watcher.fileChanged.connect(self.recalculate_and_notify)
        self._change_callback = callback

        # We store the contents of all files in an array so we can quickly
        # rebuild the concatenated stylesheet when needed
        self._file_contents = [self.read_file(path) for path in self.filepaths]

        # Run callback now with initial file contents
        self.recalculate_and_notify()


    def recalculate_and_notify(self, changed_filepath=None):
        if changed_filepath != None:
            logging.info("CSS file changed and is being reloaded: %s" % changed_filepath)
            self._file_contents[self.filepaths.index(changed_filepath)] = self.read_file(changed_filepath)
        if self.change_callback != None:
            self.change_callback("\n".join(self._file_contents))

    def read_file(self, filepath):
        with open(filepath, 'r') as stylefile:
            return stylefile.read()

    @property
    def filepaths(self):
        return self._filepaths

    ## A lambda that takes a concatenated stylesheet string as a parameter.
    # This is called once at init time and again any time a css file changes on
    # disk.
    @property
    def change_callback(self):
        return self._change_callback
