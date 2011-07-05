#!/usr/bin/python

import logging
from config import *
from rete import *
from window import *

class Illuminator:
    def __init__(self):
        logging.basicConfig()
        self.config = Config()
        self.rete = Rete(self)
        self.finestra = Window(self)
    


    def run(self):
        self.finestra.run()

if __name__ == '__main__':
    ill = Illuminator()
    net = Rete(ill)

    ill.run()
    
