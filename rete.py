
import socket

class Rete:
    def __init__(self, io):
        self.io = io

    """
    metodi di interfacciamento con l'interfaccia grafica
    """

    def leggi_stato(self):
        return 0

    def aumenta_luce(self):
        pass

    def riduci_luce(self):
        pass

    def accendi(self):
        pass

    def spegni(self):
        pass

    """
    """

    def _connetti(self):
        pass

    def _disconnetti(self):
        pass

    def _invia(self, data):
        pass

    def _ricevi(self):
        pass

