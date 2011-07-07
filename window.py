
from Tkinter import *

class Window():
    def __init__(self, io):
        self.io = io
        self.__f = Tk()
        self.__f.title("MyEls " + self.io.config.version)
        self.__f.resizable(FALSE, FALSE)
        self.__f.geometry("%dx%d+%d+%d" % (300, 150,0,0)) 
        #self.__f.wm_iconbitmap("icon.ico") 
        
        self.frameR0 = Frame(self.__f, width="300", height="25", bd=2, relief= GROOVE) 
        self.frameR1 = Frame(self.__f,bg="red",    width="300", height="50") 
        self.frameR2C0 = Frame(self.__f,bg="blue",   width="50", height="50")
        self.frameR2C1 = Frame(self.__f,bg="green",  width="200", height="50")
        self.frameR2C2 = Frame(self.__f,bg="orange",   width="50", height="50")
        self.frameR3 = Frame(self.__f, width="300", height="25", bd=2, relief=GROOVE)
         
        self.frameR0.grid(row=0, column=0,columnspan=3) 
        self.frameR1.grid(row=1, column=0, columnspan=3)
        self.frameR2C0.grid(row=2, column=0)
        self.frameR2C1.grid(row=2, column=1) 
        self.frameR2C2.grid(row=2, column=2)
        self.frameR3.grid(row=3, column=0, columnspan=3)
        # creata tutta la griglia di frame ora la riempio
        self.__ButtonAction = Button(self.frameR1, text="Azione" )
        self.__ButtonAction.pack()
        self.__ButtonAction['command'] = self.ButtonClickAction

        self.__ButtonAction = Button(self.frameR2C0, text="-" )
        self.__ButtonAction.pack()
        self.__ButtonAction['command'] = self.ButtonClickMeno

        self.__ButtonAction = Button(self.frameR2C2, text="+" )
        self.__ButtonAction.pack()
        self.__ButtonAction['command'] = self.ButtonClickPiu



        self.__StatusBar = Label(self.frameR3, text="Connessione in corso..")
        self.__StatusBar.pack()    


# Metodi Ascoltatori Pulsanti    
    def ButtonClickAction(self):
        print "Luca gay azione"
    def ButtonClickMeno(self):
        print "Luca gay meno"
    def ButtonClickPiu(self):
        print "Luca gay piu"


    def run(self):
        self.__f.mainloop()
