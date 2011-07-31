from Tkinter import *
import tkMessageBox
import logging

import rete

log = logging.getLogger('window')

class Window():
    def __init__(self, io):
        self.io = io
        self._luceAccesa = False
        #self._configured = False
        self.__f = Tk()
        self.screenW = self.__f.winfo_screenwidth()
        self.screenH = self.__f.winfo_screenheight()
        windW = 300
        windH = 100
        posX = (self.screenW - windW)/2
        posY = (self.screenH - windH)/2
        
        self.__f.title("Illuminator " + self.io.config.version)
        self.__f.resizable(FALSE, FALSE)
        self.__f.geometry("%dx%d+%d+%d" % (windW, windH, posX, posY)) 
        #self.__f.wm_iconbitmap(bitmap="@icon2.bmp") 
        self.__f.wm_iconbitmap(bitmap="@icon.xbm") 
         
        self.__ButtonAction = Button(self.__f, text="Connessione in corso..", width="100", height="100" )
        self.__ButtonAction.pack()
        self.__ButtonAction['command'] = self.ButtonClickAction          
        self.__f.bind("<Return>", self.shortCutRoot)
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
        self.AboutWindow = a = Toplevel(self.__f)
        windW = 270
        windH = 320
        posX = (self.screenW - windW)/2
        posY = (self.screenH - windH)/2
        a.geometry("%dx%d+%d+%d" % (windW, windH, posX, posY)) 
        a.title('Informazioni')        
        a.wm_iconbitmap(bitmap="@icon.xbm") 
        
        self.__fR0 = Frame(a, width="450", height="125")   
        self.__fR1 = Frame(a, width="450", height="20")
        self.__fR2 = Frame(a, width="450", height="30")
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
        a.bind("<Escape>", self.shortCutAbout)
        self.__f.iconify()
        
    
    def shortCutAbout(self, event):
        if event.keysym == "Escape":
            self.CloseAboutWindowButton_Click()    
        
        
    def CloseAboutWindowButton_Click(self):
        self.AboutWindow.destroy()
        self.__f.deiconify()
        
    def leggiConfig(self):
        self.ConfigWindow = w = Toplevel(self.__f)
        windW = 250
        windH = 100
        posX = (self.screenW - windW)/2
        posY = (self.screenH - windH)/2
        w.geometry("%dx%d+%d+%d" % (windW, windH, posX, posY))
        
        
        self.__wR0C0 = Frame(w, width="250", height="70")   
        self.__wR0C1 = Frame(w, width="250", height="70")
        self.__wR1C0 = Frame(w, width="250", height="70")   
        self.__wR1C1 = Frame(w, width="250", height="70")
        self.__wR2C0 = Frame(w, width="250", height="70")   
        self.__wR2C1 = Frame(w, width="250", height="70")
        self.__wR3C0 = Frame(w, width="250", height="70")   
        self.__wR3C1 = Frame(w, width="250", height="70")
        
        self.__wR0C0.grid(row=0, column=0)
        self.__wR0C1.grid(row=0, column=1)
        self.__wR1C0.grid(row=1, column=0)
        self.__wR1C1.grid(row=1, column=1)
        self.__wR2C0.grid(row=2, column=0)
        self.__wR2C1.grid(row=2, column=1)
        self.__wR3C0.grid(row=3, column=0)
        self.__wR3C1.grid(row=3, column=1)
        
        
        ip_Label = Label (self.__wR0C0, text='Indirizzo Ip')
        ip_Label.pack(side= LEFT)
        self.ip_Text = Entry(self.__wR0C1, width=15)
        self.ip_Text.pack()
        
        porta_Label = Label (self.__wR1C0, text='Porta')
        porta_Label.pack(side= LEFT)
        self.porta_Text = Entry(self.__wR1C1, width=15)
        self.porta_Text.pack()
        
        luce_Label = Label (self.__wR2C0, text='Indirizzo SCS')
        luce_Label.pack(side= LEFT)
        self.luce_Text = Entry(self.__wR2C1, width=15)
        self.luce_Text.pack()
        
        okb = Button(self.__wR3C0, text='Cancella', command=self.__f.destroy)
        okb.pack()
        
        okb = Button(self.__wR3C1, text='Ok', command=self.configDestroy)
        okb.pack()
        
        w.bind("<Return>", self.shortCut)
        w.bind("<Escape>", self.shortCut)
        
        w.protocol("WM_DELETE_WINDOW", self.__f.destroy)
        w.title('Configurazione')
        self.__f.withdraw()
        
    def shortCut(self, event):
        if event.keysym == "Return":
            self.configDestroy()
        elif event.keysym == "Escape":
            self.__f.destroy()
        

    def configDestroy(self):
        """
        recupera i dati della configurazione inseriti
        se sono validi scrive la configurazione e distrugge il widget,
        altrimenti rimane impalato finche i dati sono giusti
        """
        error = False
        host = self.ip_Text.get()
        porta = self.porta_Text.get()
        luce = self.luce_Text.get()

        # validazione IP
        try:
            ip_fields = host.split('.')
            assert len(ip_fields) == 4
            for n in ip_fields:
                assert int(n) >= 0
                assert int(n) <= 255
        except (AssertionError, ValueError):
            error = True
            log.exception('validando IP')

        # validazione porta
        try:
            int(porta)
        except ValueError:
            error = True
            log.exception('validando la porta')

        # validazione punto luce
        try:
            if luce.startswith('#'):
                int(luce[1:])
            else:
                int(luce)
        except ValueError:
            error = True
            log.exception('validando il punto luce')

        if error:
            # Error
            print 'error'
            tkMessageBox.showerror("Errore", "Errore nella configurazione. \nRicontrollare parametri.")
            self.ConfigWindow.grab_set()
            self.ConfigWindow.lift()
        else:
            d = {'APl':luce,
                 'Ip':host,
                 'Porta':porta}

            self.io.config.write_config(d)
            self.io.config.read_config()
            self.ConfigWindow.destroy()
            self.aggiornaStato()
            self.__f.deiconify()
    def aggiornaStato(self):
        try:
            st = self.io.rete.leggi_stato()
        except rete.Error, e:
            self.__ButtonAction['text'] =  str(e)
            tkMessageBox.showerror('Errore', str(e))
            return
        #if not self._luceAccesa:
        if st > 0:
            self.__ButtonAction['text'] = 'Spegni'
            self._luceAccesa = True
        else:
            self.__ButtonAction['text'] = 'Accendi'
            self._luceAccesa = False

# Metodi Ascoltatori Pulsanti e slider
    def shortCutRoot(self, event):
        if event.keysym == "Return":
            self.ButtonClickAction()
            
    def ButtonClickAction(self):
        try:
            if self._luceAccesa:
                self.io.rete.spegni()
            else:
                self.io.rete.accendi()
        except rete.Error, e:
            self.__ButtonAction['text'] =  str(e)
            tkMessageBox.showerror('Errore', str(e))
            return           
        self.aggiornaStato()

    def windowReady(self):
        # solo la prima volta che la finestra viene configurata
        # controllo che abbia una configurazione valida
        #if not self._configured:
            if self.io.config.check_config():
                #self.aggiornaStato()
                self.__f.after(100, self.aggiornaStato)
                self.__f.protocol("WM_TAKE_FOCUS", self.windowReady)
        #    self._configured = True

    def run(self):
        #self.__f.bind('<Configure>', self.windowReady)
        self.__f.after_idle(self.windowReady)
        #self.__f.protocol("WM_TAKE_FOCUS", self.windowReady)
        self.__f.mainloop()

