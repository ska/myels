#!/usr/bin/python

import socket
import time
from Tkinter import *
import logging


class Finestra:
    __f=''
    __s=''
    __StatusBar=''
    __ButtonAcition=''
    __Slider=''
    __APl='21'
    __active=FALSE
    __Ip='192.168.1.35'
    __Porta=20000
    __version= '0.2b'
    __sliderStatus= 0
    
    def __init__(self):
        self.creaFinestra()
        self.connetti()
        self.primaLetturaStato()
        self.setSlider()
        self.disconnetti()
        self.__f.mainloop()
                        
    def creaFinestra(self):
        self.__f = Tk()
        self.__f.title("MyEls " + self.__version)
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
   
    def connetti(self):
        try:
            self.__s=socket.socket( socket.AF_INET, socket.SOCK_STREAM)
            self.__s.connect((self.__Ip, self.__Porta))
            ack = self.__s.recv(6)
            if(ack != "*#*1##"):                
                self.__StatusBar["text"] = "Non connesso"
            else:
                self.__StatusBar["text"] = "Connesso a " + self.__Ip
        except socket.error, msg:        
            logging.exception("Non connesso connessione")
            self.__StatusBar["text"] = "Non connesso"
            
            
    def primaLetturaStato(self):
        try:
            self.__s.send("*#1*"+ self.__APl +"##")
            status = self.__s.recv(128)
            status = status[3:5]
            if status[1] == "*":
                status = status[0]        
            status = int(status)        
            self.__active = TRUE
            
            if status == 0:
                self.__ButtonAction["text"] = "Accendi"
            else:
                self.__ButtonAction["text"] = "Spegni"
            self.__sliderStatus = status
            
        except:
            logging.exception("Errore Lettura Primo Stato")

    def leggiStato(self):
        try:
            self.connetti()
            self.__s.send("*#1*"+ self.__APl +"##\0")
            status =  self.__s.recv(9)
            self.__s.recv(128)
            status = status[3:5]
            if status[1] == '*':
                status = status[0]
            self.__sliderStatus = int( status )
            self.setSlider()
            self.disconnetti()
        except:
            logging.exception("Errore leggiStato")     
             
    def setSlider(self):
        self.__Slider.set(self.__sliderStatus)
        if self.__sliderStatus != 0:
            self.__ButtonAction["text"] = "Spegni"
        else:
            self.__ButtonAction["text"] = "Accendi" 
 
    
                     
    def SliderChange(self, x):
        if self.__active == TRUE:
            self.leggiStato()
            self.connetti()
            self.__s.send("*1*"+ x +"*"+ self.__APl +"##")
            self.disconnetti()
            self.leggiStato()
            
    def ButtonClickAction(self):
        try:           
            self.leggiStato()
            self.connetti()
            if self.__sliderStatus != 0:
                cmd = "*1*0*"+ self.__APl +"##"
                self.__s.send(cmd)
        
            else:
                cmd = "*1*1*"+ self.__APl +"##"
                self.__s.send(cmd)       
            self.disconnetti()
            self.leggiStato()
        except:
            logging.exception("Errore leggiStato")    

    def ButtonClickPiu(self):
        self.connetti()
        self.__s.send("*1*30*"+ self.__APl +"##")
        self.__s.recv(6) 
        self.leggiStato()
        self.setSlider()
        self.disconnetti()
        
    def ButtonClickMeno(self):
        self.connetti()
        self.__s.send("*1*31*"+ self.__APl +"##")
        self.__s.recv(6)
        self.leggiStato()
        self.setSlider()
        self.disconnetti()
        
    def disconnetti(self):
        self.__s.close()
    
if __name__ == '__main__':  
    logging.basicConfig()
    finestra = Finestra()
