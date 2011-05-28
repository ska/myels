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
    __version= '0.1b'
    
    def __init__(self):
        self.creaFinestra()
        self.connetti()
        self.leggiStato()
        self.disconnetti()
        self.__f.mainloop()
                        
    def creaFinestra(self):
        self.__f = Tk()
        self.__f.title("MyEls " + self.__version)
        self.__f.geometry('300x200')
        self.__f.resizable(FALSE, FALSE)
        self.__StatusBar = Label(self.__f, text="Connessione in corso..")
        self.__StatusBar.pack({"side":"bottom", "expand":"no"})
        
        self.__ButtonAccendi = Button(self.__f, text="Accendi")
        self.__ButtonAccendi.pack({"side":"top", "padx":1, "pady":0})
        self.__ButtonAccendi['command'] = self.ButtonClickAccendi
        
        self.__ButtonSpegni = Button(self.__f, text="Spegni")
        self.__ButtonSpegni.pack({"side":"top", "padx":2, "pady":20})
        self.__ButtonSpegni['command'] = self.ButtonClickSpegni
        
        self.__Slider = Scale(self.__f, from_=0, to=10, resolution=1, label='Dimmer', command = self.SliderChange, orient=HORIZONTAL)
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
                self.__StatusBar["text"] = "Connesso"
        except:        
            print "Non connesso 1"
            self.__StatusBar["text"] = "Non connesso"

    def leggiStato(self):
        try:
            self.__s.send("*#1*"+ self.__APl +"##")
            status = self.__s.recv(9)
            status = status[3]
            print "status:" + status
            if status >= 0:
                self.__Slider.set(status)
                self.__active=TRUE
        except:  # cattura solo socket error
            print "Non connesso 2"
            self.__StatusBar["text"] = "Non connesso"               
                              
    def SliderChange(self, x):
        if self.__active == TRUE:
            self.connetti()
            self.__s.send("*1*"+ x +"*"+ self.__APl +"##")
            self.disconnetti()
            
    def ButtonClickAccendi(self):
        self.connetti()
        self.__s.send("*1*1*"+ self.__APl +"##")
        self.disconnetti()
        
    def ButtonClickSpegni(self):
        self.connetti()
        self.__s.send("*1*0*"+ self.__APl +"##")
        self.disconnetti()

    def disconnetti(self):
        self.__s.close()
    
if __name__ == '__main__':
	finestra = Finestra()
