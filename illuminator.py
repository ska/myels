#!/usr/bin/python

import logging
from config import *
from rete import *
from window import *

class Illuminator:
    def __init__(self):
        self.config = Config(self)
        self.rete = Rete(self)
        self.finestra = Window(self)

    def run(self):
        self.finestra.run()

def main():
    if sys.platform == 'win32':
        # entra nella directory temporanea di lavoro
        import os
        tmpdir = os.environ.get('_MEIPASS2', None)
        if tmpdir:
            os.chdir(tmpdir)
    io = Illuminator()
    io.run()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()

