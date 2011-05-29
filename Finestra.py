#!/usr/bin/python

import socket
import time
from Tkinter import *

class Finestra:
    __f=''
    __s=''
    __StatusBar=''
    __ButtonAccendi=''
    __ButtonSpegni=''
    __Slider=''
    __APl='21'
    __active=FALSE
    __Ip='192.168.1.35'
    __Porta=20000
    __version= '0.2b'
    __s0=""
    
    def __init__(self):
        self.creaFinestra()
        self.connetti()
        self.setSlider(self.primaLetturaStato())
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
        
        #self.__ButtonAccendi = Button(self.frameR1C0, text="Accendi" )
        #self.__ButtonAccendi.pack({"side":"top", "padx":1, "pady":0})
        #self.__ButtonAccendi['command'] = self.ButtonClickAccendi
        
        #self.__ButtonSpegni = Button(self.frameR1C2, text="Spegni")
        #self.__ButtonSpegni.pack({"side":"top", "padx":2, "pady":20})
        #self.__ButtonSpegni['command'] = self.ButtonClickSpegni
        
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
                print "Non connesso 0"
                self.__StatusBar["text"] = "Non connesso"
            else:
                self.__StatusBar["text"] = "Connesso a " + self.__Ip
        except socket.error, msg:        
            print "Non connesso 1"
            self.__StatusBar["text"] = "Non connesso"
        except:
            print "Non connesso 2"
            self.__StatusBar["text"] = "Non connesso"
            
            
    def primaLetturaStato(self):
        try:
            self.__s.send("*#1*"+ self.__APl +"##")
            status = self.__s.recv(128)
            print "status 1:" + status
            val = status[3:5]
            if val[1] == "*":
                val = val[0]                
            print "Val " + val
            self.__active = TRUE
            
            if val == 0:
                print "spento"
                self.__ButtonAction["text"] = "Accendi"
            else:
                print "Acceso"
                self.__ButtonAction["text"] = "Spegni"
            print "esco con val: " + val
            return val
            
        except:
            print "Non connesso 3"
            self.__StatusBar["text"] = "Non connesso"
            return 0       
    
    def leggiStato(self):
        try:
            self.__s.send("*#1*"+ self.__APl +"##")
            status = self.__s.recv(128)
            #status = status[3]
            print "status 1:" + status
            status = self.__s.recv(128)
            print "status 2:" + status
            
            val = status[3:5]
            if val[1] == "*" or val[1] == "#":
                val = val[0] 
            print "esco con val2: " + val    
            return val    
            
            #self.__Slider.set(val)
                       
        except:
            print "Non connesso 4"
            self.__StatusBar["text"] = "Non connesso"         
            return 0 
             
    def setSlider(self, val):
        print "Pippo: " + val
        self.__Slider.set(val)  
    
                     
    def SliderChange(self, x):
        if self.__active == TRUE:
            self.connetti()
            self.__s.send("*1*"+ x +"*"+ self.__APl +"##")
            self.disconnetti()
            
    def ButtonClickAction(self):
        self.connetti()
        val = self.leggiStato()
        if val != 0:
            print "action: " + val
            self.__s.send("*1*0*"+ self.__APl +"##")
        else:
            print "action: " + val
            self.__s.send("*1*1*"+ self.__APl +"##")
        
        self.leggiStato()
        self.disconnetti()
        
            
    def ButtonClickAccendi(self):
        self.connetti()
        self.__s.send("*1*1*"+ self.__APl +"##")
        self.leggiStato()
        self.disconnetti()
        
    def ButtonClickSpegni(self):
        self.connetti()
        self.__s.send("*1*0*"+ self.__APl +"##")
        self.leggiStato()
        self.disconnetti()
        
    def ButtonClickPiu(self):
        self.connetti()
        self.__s.send("*1*30*"+ self.__APl +"##")
        self.setSlider(self.leggiStato())
        self.disconnetti()
        
    def ButtonClickMeno(self):
        self.connetti()
        self.__s.send("*1*31*"+ self.__APl +"##")
        self.setSlider(self.leggiStato())
        self.disconnetti()
        
    def disconnetti(self):
        self.__s.close()
    
if __name__ == '__main__':
	finestra = Finestra()
