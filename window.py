
from Tkinter import *

class Window():
    def __init__(self, io):
        self.io = io
        self.__f = Tk()
        self.__f.title("MyEls " + self.io.config.version)
        self.__f.resizable(FALSE, FALSE)
        self.__f.geometry("%dx%d+%d+%d" % (300, 150,0,0)) 
        self.__f.wm_iconbitmap(bitmap="@icon.xbm") 
        
        self.frameR0 = Frame(self.__f, width="300", height="25", bd=2, relief= GROOVE) 
        self.frameR1 = Frame(self.__f,bg="red",    width="300", height="50") 
        self.frameR2 = Frame(self.__f, width="300", height="25", bd=2, relief=GROOVE)
         
        self.frameR0.grid(row=0, column=0) 
        self.frameR1.grid(row=1, column=0)
        self.frameR2.grid(row=2, column=0)
        # creata tutta la griglia di frame ora la riempio
        self.__ButtonAction = Button(self.frameR1, text="Azione" )
        self.__ButtonAction.pack()
        self.__ButtonAction['command'] = self.ButtonClickAction

        self.__StatusBar = Label(self.frameR2, text="Connessione in corso..")
        self.__StatusBar.pack()    


# Metodi Ascoltatori Pulsanti e slider   
    def ButtonClickAction(self):
        print "Luca gay azione"

    def run(self):
        self.__f.mainloop()
