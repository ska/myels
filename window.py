
from Tkinter import *

class Window():
    def __init__(self, io):
        self.io = io
        self._luceAccesa = False
        self._configured = False
        self.__f = Tk()
        self.__f.title("MyEls " + self.io.config.version)
        self.__f.resizable(FALSE, FALSE)
        self.__f.geometry("%dx%d+%d+%d" % (300, 110,0,0)) 
        self.__f.wm_iconbitmap(bitmap="@icon.xbm") 
        
        #self.frameR0 = Frame(self.__f, width="300", height="35", bd=2, relief= GROOVE) 
        self.frameR1 = Frame(self.__f, width="300", height="50") 
        self.frameR2 = Frame(self.__f, width="300", height="25", bd=2, relief=GROOVE)
         
        #self.frameR0.grid(row=0, column=0) 
        self.frameR1.grid(row=1, column=0)
        self.frameR2.grid(row=2, column=0)
        # creata tutta la griglia di frame ora la riempio
        self.__ButtonAction = Button(self.frameR1, text="Azione" )
        self.__ButtonAction.pack()
        self.__ButtonAction['command'] = self.ButtonClickAction

        self.__StatusBar = Label(self.frameR2, text="Connessione in corso..")
        self.__StatusBar.pack()    
        
        # Barra dei menu
        self.__menuBar = Menu(self.__f)
        # Barra dei menu file
        self.__fileMenu = Menu(self.__menuBar, tearoff=0)
        self.__menuBar.add_cascade(label="File", menu=self.__fileMenu)
        self.__fileMenu.add_command(label="Esci", command=self.__f.quit)
        # Barra dei menu help
        self.__helpMenu = Menu(self.__menuBar, tearoff=0)
        self.__menuBar.add_cascade(label="Aiuto", menu=self.__helpMenu)
        self.__helpMenu.add_command(label="Informazioni", command=self.HelpAbout)
          
        self.__f.config(menu=self.__menuBar)
        
        
    ## Finestra di info        
    def HelpAbout(self):
        self.AboutWindow = Toplevel(self.__f, height=300, width=300)
        self.AboutWindow.title('Informazioni')
        self.AuthorLabel = Label(self.AboutWindow, text='Author: xxxx')
        #self.AuthorLabel.pack()
        self.CloseAboutWindowButton = Button(self.AboutWindow, text='Chiudi', command=self.CloseAboutWindowButton_Click)
        self.CloseAboutWindowButton.pack()
        self.AboutWindow.grab_set()  # questo rende la finestra "modale"

    def CloseAboutWindowButton_Click(self):
        self.AboutWindow.destroy() 

    def leggiConfig(self):
        self.ConfigWindow = w = Toplevel(self.__f, height=100, width=1000)

        okb = Button(w, text='Ok', command=self.configDestroy)
        okb.pack()

        w.protocol("WM_DELETE_WINDOW", self.configDestroy)
        w.title('Configurazione')
        w.grab_set()
        w.lift()

    def configDestroy(self):
        d = {}
        # TODO
        # recupera i dati della configurazione inseriti
        # se sono validi scrive la configurazione e distrugge il widget,
        # altrimenti rimane impalato finche i dati sono giusti
        self.io.config.write_config(d)
        self.io.config.read_config()
        self.ConfigWindow.destroy()
        self.aggiornaStato()

    def aggiornaStato(self):
        st = self.io.rete.leggi_stato()
        #if not self._luceAccesa:
        if st > 0:
            self.__ButtonAction['text'] = 'Spegni'
            self._luceAccesa = True
        else:
            self.__ButtonAction['text'] = 'Accendi'
            self._luceAccesa = False

# Metodi Ascoltatori Pulsanti e slider   
    def ButtonClickAction(self):
        if self._luceAccesa:
            self.io.rete.spegni()
        else:
            self.io.rete.accendi()
        self.aggiornaStato()
        print "Luca gay azione"

    def windowReady(self, event):
        # solo la prima volta che la finestra viene configurata
        # controllo che abbia una configurazione valida
        if not self._configured:
            if self.io.config.check_config():
                self.aggiornaStato()
            self._configured = True

    def run(self):
        self.__f.bind('<Configure>', self.windowReady)
        #self.__f.protocol("WM_TAKE_FOCUS", self.windowReady)
        self.__f.mainloop()

