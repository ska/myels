#!/usr/bin/python

import logging

class Illuminator:
    def __init__(self):
        logging.basicConfig()
        self.config = Config()
        self.rete = Rete()
        self.finestra = Window(self)
        
    def run(self):
        pass

if __name__ == '__main__':
    io = Illuminator()
    io.run()

