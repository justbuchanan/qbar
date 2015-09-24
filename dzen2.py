#!/usr/bin/env python3

import subprocess

MAIN_FONT="DejaVu Sans Mono for Powerline"
PANEL_HEIGHT=30


def fa_icon(char):
    return "^fn(FontAwesome)%s^fn(%s)" % (char, MAIN_FONT)

def md_icon(char):
    return "^fn(MaterialIcons-Regular)%s^fn(%s)" % (char, MAIN_FONT)


class BarItem():
    # returns a dzen2-formatted string
    def render(self):
        pass


class SimpleItem(BarItem):
    def render(self):
        out = ""
        if self.icon != None: out += fa_icon(self.icon) + " "
        if self.text != None: out += self.text

    @property
    def icon(self):
        return self._icon

    @property
    def text(self):
        return self._text
    

class Panel():
    def __init__(self):
        monitor_index=1
        args = ['dzen2', '-h', str(PANEL_HEIGHT), '-p', '-x', '0', '-xs', str(monitor_index)]
        self.dzen2 = subprocess.Popen(args, stdin=subprocess.PIPE)

    def render(self):
        return "hello"


    def run(self):
        while True:
            content = "%s\n" % self.render()
            self.dzen2.communicate(content.encode('utf-8'))


def main():
    panel = Panel()
    panel.run()


if __name__ == '__main__':
    main()
