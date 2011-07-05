
from Tkinter import *

class Window():
    def __init__(self, io):
        self.io = io
        self.__f = Tk()
        self.__f.title("MyEls " + self.io.config.version)
        self.__f.resizable(FALSE, FALSE)
        

    def run(self):
        self.__f.mainloop()
