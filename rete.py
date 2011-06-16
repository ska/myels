
import socket
import logging

CMD_ACK = "*#*1##"
CMD_GETSTATUS = "*#1*%s##" # APl
CMD_ON = "*1*1*%s##" # APl
CMD_OFF = "*1*0*%s##" # APl
CMD_MORE = "*1*30*%s##" #APl
CMD_LESS = "*1*31*%s##" #APl


class Rete:
    def __init__(self, io):
        self.io = io
        self.log = logging.getLogger('rete')
        self._s = None

    """
    metodi di interfacciamento con l'interfaccia grafica
    """

    def leggi_stato(self):
        self._connetti()
        cmd = CMD_GETSTATUS % self.io.config.APl
        self._invia(cmd)
        data = self._ricevi()
        data = data.split('*')
        # ['', '1', '0', '21##']
        self._disconnetti()
        return int(data[2])

    def aumenta_luce(self):
        self._connetti()
        cmd = CMD_MORE % self.io.config.APl
        self._invia(cmd)
        self._leggi_ack()
        self._disconnetti()

    def riduci_luce(self):
        self._connetti()
        cmd = CMD_LESS % self.io.config.APl
        self._invia(cmd)
        self._leggi_ack()
        self._disconnetti()

    def accendi(self):
        self._connetti()
        cmd = CMD_ON % self.io.config.APl
        self._invia(cmd)
        self._leggi_ack()
        self._disconnetti()

    def spegni(self):
        self._connetti()
        cmd = CMD_OFF % self.io.config.APl
        self._invia(cmd)
        self._leggi_ack()
        self._disconnetti()

    """
    """

    def _connetti(self):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.connect((self.io.config.Ip, self.io.config.Porta))
        self._leggi_ack()

    def _disconnetti(self):
        self._s.close()
        self._s = None

    def _leggi_ack(self):
        ack = self._ricevi(len(CMD_ACK))
        if ack != CMD_ACK:
            # raise AckError?
            self.log.error('Ack errato: %s' %ack)

    def _invia(self, data):
        try:
            self.log.debug('invio %s' %data)
            sent = self._s.send(data)
        except socket.error:
            self.log.exception('inviando %s' %data)

    def _ricevi(self, maxb=1024):
        try:
            data = self._s.recv(maxb)
        except socket.error:
            self.log.exception('ricevendo %s' %maxb)
            # raise
            return ''
        else:
            self.log.debug('ricevo %s' %data)
            return data


if __name__=='__main__':
    # inizializzo cosi posso richiamarlo in una shell pyhton
    import sys
    import config
    logging.basicConfig(level=logging.DEBUG)
    class FakeIlluminator():
        config = config.Config()

    io = FakeIlluminator()
    if len(sys.argv) > 1:
        io.config.Ip = sys.argv[1]
    rete = Rete(io)

