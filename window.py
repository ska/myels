from Tkinter import *

class Window():
    def __init__(self, io):
        self.io = io
        self._luceAccesa = False
        self.__f = Tk()
        self.__f.title("MyEls " + self.io.config.version)
        self.__f.resizable(FALSE, FALSE)
        self.__f.geometry("%dx%d+%d+%d" % (300, 110,0,0)) 
        #self.__f.wm_iconbitmap(bitmap="@icon2.bmp") 
        self.__f.wm_iconbitmap(bitmap="@icon.xbm") 
         
        self.__ButtonAction = Button(self.__f, text="Azione", width="100", height="100" )
        self.__ButtonAction.pack()
        self.__ButtonAction['command'] = self.ButtonClickAction          
        
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
        self.__AboutWindow = Toplevel(self.__f, height="175", width="450")
        self.__AboutWindow.title('Informazioni')        
        self.__AboutWindow.wm_iconbitmap(bitmap="@icon.xbm") 
        
        self.__fR0 = Frame(self.__AboutWindow, width="450", height="125")   
        self.__fR1 = Frame(self.__AboutWindow, width="450", height="20")
        self.__fR2 = Frame(self.__AboutWindow, width="450", height="30")
        self.__fR0.grid(row=0, column=0)
        self.__fR1.grid(row=1, column=0)
        self.__fR2.grid(row=2, column=0)
        
        self.__photo = PhotoImage(file="logo.gif", width=150, height=125)
        self.__logo = Label(self.__fR0, image=self.__photo)
        self.__logo.photo = self.__photo
        self.__logo.pack()
        
        self.__title = Label(self.__fR1, font=("Helvetica", 16), text='Illuminator ' + self.io.config.version)
        self.__title.pack()
        self.__descr = Label(self.__fR1, font=("Helvetica", 10), text='Programma per il comando di un punto luce \n su sistema domotico MYHOME BTICINO \n\n')
        self.__descr.pack()
        self.__autore1 = Label(self.__fR1, font=("Helvetica", 10), text='Luca Dariz <luca.dariz@gmail.com>')
        self.__autore1.pack()
        self.__autore2 = Label(self.__fR1, font=("Helvetica", 10), text='Luigi Scagnet <luigi.scagnet@gmail.com>')
        self.__autore2.pack()
        
        self.__CloseAboutWindowButton = Button(self.__fR2, text='Chiudi', command=self.CloseAboutWindowButton_Click)
        self.__CloseAboutWindowButton.pack()
        #self.__AboutWindow.grab_set()  # questo rende la finestra "modale"

    def CloseAboutWindowButton_Click(self):
        self.__AboutWindow.destroy()        
                                                                                                  
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

    def run(self):
        self.aggiornaStato()
        self.__f.mainloop()
        
