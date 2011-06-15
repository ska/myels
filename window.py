
from Tkinter import *

class Window():
    def __init__(self, io):
        self.io = io
        self.__f = Tk()
        self.__f.title("MyEls " + self.io.config.version)
        self.__f.resizable(FALSE, FALSE)
        #self.__f.wm_iconbitmap("icon.png")
        
        self.frameR0 = Frame(self.__f)
        self.frameR1C0 = Frame(self.__f)
        self.frameR1C1 = Frame(self.__f)
        self.frameR1C2 = Frame(self.__f)
        self.frameR2C0 = Frame(self.__f)
        self.frameR2C1 = Frame(self.__f)
        self.frameR2C2 = Frame(self.__f)
        self.frameR3 = Frame(self.__f)
        
        self.frameR0.configure( width="300", height="25")
        self.frameR1C0.configure( width="100", height="50")
        self.frameR1C1.configure( width="100", height="50")
        self.frameR1C2.configure( width="100", height="50")        
        self.frameR2C0.configure( width="100", height="150")
        self.frameR2C1.configure( width="100", height="150")
        self.frameR2C2.configure( width="100", height="150")        
        self.frameR3.configure( width="200", height="30", bd=1, relief=GROOVE)
        
        self.frameR0.grid(row=0, column=0, columnspan=3)
        self.frameR1C0.grid(row=1, column=0)
        self.frameR1C1.grid(row=1, column=1)
        self.frameR1C2.grid(row=1, column=2)
        self.frameR2C0.grid(row=2, column=0)
        self.frameR2C1.grid(row=2, column=1)
        self.frameR2C2.grid(row=2, column=2)
        self.frameR3.grid(row=3, column=0, columnspan=3)
       
        menubar = Menu(self.frameR0)
        
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Preferenze")
        filemenu.add_separator()
        filemenu.add_command(label="Esci")
        menubar.add_cascade(label="File", menu=filemenu)
        self.__f.config(menu=menubar)
          
        self.__StatusBar = Label(self.frameR3, text="Connessione in corso..")
        self.__StatusBar.pack()                        
        
        self.__ButtonAction = Button(self.frameR1C0, text="Accendi" )
        self.__ButtonAction.pack({"side":"top", "padx":1, "pady":0})
        self.__ButtonAction['command'] = self.ButtonClickAction
        
        self.__ButtonPiu = Button(self.frameR2C2, text="+")
        self.__ButtonPiu.pack({"side":"top", "padx":2, "pady":2})
        self.__ButtonPiu['command'] = self.ButtonClickPiu
        
        self.__ButtonMeno = Button(self.frameR2C0, text="-")
        self.__ButtonMeno.pack({"side":"top", "padx":2, "pady":2})
        self.__ButtonMeno['command'] = self.ButtonClickMeno
        
        self.__Slider = Scale(self.frameR2C1, from_=0, to=10, resolution=1, label='Dimmer', command = self.SliderChange, orient=HORIZONTAL)
        self.__active=FALSE
        self.__Slider.pack()

