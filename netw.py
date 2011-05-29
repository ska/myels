import socket

class Finestra:
    __s=''
    
    
    
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
            
            
        
    def disconnetti(self):
        self.__s.close()
