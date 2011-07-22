
import socket
import logging

CMD_ACK = "*#*1##"
CMD_GETSTATUS = "*#1*%s##" # APl
CMD_ON = "*1*1*%s##" # APl
CMD_OFF = "*1*0*%s##" # APl
CMD_MORE = "*1*30*%s##" #APl
CMD_LESS = "*1*31*%s##" #APl

log = logging.getLogger('rete')

class OpenMSG(object):
    def __init__(self, data=None):
        self.is_ack = False
        self.is_nack = False
        self.is_std = False
        self.is_sts_req = False
        self.is_dim_req = False
        self.is_dim_wr = False
        self.who = None
        self.what = None
        self.where = None
        self.dim = None
        self.vals = []
        if data:
            self.parse_msg(data)

    def parse_msg(self, data):
        """ riconosce i vari tipi di messaggio OpenWebNet """
        if data.endswith('##'):
            data = data[:-2]
        if data.startswith('*#'):
            if (len(data) > 2) and (data[2] == '*'):
                # ACK/NACK
                #if data[3] == '1':
                if data.startswith('1', 3):
                    self.is_ack = True
                elif data.startswith('0', 3):
                    self.is_nack = True
                else:
                    log.error('errore di parsing 3: %s' %(data,))
            else:
                data = data[2:].split('*')
                if len(data) == 2:
                    # STATUS
                    self.is_sts_req = True
                    self._parse_status_request(data)
                elif len(data) == 3:
                    # DIM REQ
                    self.is_dim_req = True
                    self._parse_dim_request(data)
                elif (len(data) > 3) and (data[2].startswith('#')):
                    # DIM WRITE
                    self.is_dim_wr = True
                    self._parse_dim_write(data)
                else:
                    log.error('errore di parsing 2: %s' %(data,))
        elif data.startswith('*'):
            # STANDARD
            self.is_std = True
            data_list = data.split('*')[1:]
            self._parse_standard(data_list)
        else:
            log.error('errore di parsing: %s' %(data,))

    def _parse_standard(self, data):
        if len(data) == 3:
            self.who = data[0]
            self.what = data[1]
            self.where = data[2]
        else:
            log.error('standard: %s' %(data,))

    def _parse_status_request(self, data):
        if len(data) == 2:
            self.who = data[0]
            self.where = data[1]
        else:
            log.error('status request: %s' %(data,))

    def _parse_dim_request(self, data):
        if len(data) == 3:
            self.who = data[0]
            self.where = data[1]
            self.dim = data[2]
        else:
            log.error('dim request: %s' %(data,))

    def _parse_dim_write(self, data):
        if len(data) > 3:
            self.who = data[0]
            self.where = data[1]
            if data[2].startswith('#'):
                self.dim = data[2][1:]
                self.vals = data[3:]
                return
        log.error('dim write: %s' %(data,))

    @staticmethod
    def build_status_request(who, where):
        self = OpenMSG()
        self.is_sts_req = True
        self.who = str(who)
        self.where = str(where)
        return self

    def dump(self):
        if self.is_ack:
            return '*#*1##'
        elif self.is_nack:
            return '*#*0##'
        elif self.is_std:
            return '*%s*%s*%s##' %(self.who, self.what, self.where)
        elif self.is_sts_req:
            return '*#%s*%s##' %(self.who, self.where)
        elif self.is_dim_req:
            return '*#%s*%s*%s##' %(self.who, self.where, self.dim)
        elif self.is_dim_wr:
            vlist = '*'.join(self.vals)
            return '*#%s*%s*#%s*%s##' %(self.who, self.where, self.dim, vlist)
        else:
            log.warning('msg vuoto')
            return ''

    def __str__(self):
        return self.dump()

class Rete:
    def __init__(self, io):
        self.io = io
        self._s = None

    def single_conn(f):
        """ Ogni azione va fatta su una connessione separata """
        def wrapped_f(self, *args, **kwargs):
            try:
                self._connetti()
                try:
                    f(self, *args, **kwargs)
                except:
                    log.exception('In %s' %f.func_name)
            except:
                log.exception('Nella connessione')
            finally:
                self._disconnetti()
        return wrapped_f

    """
    metodi di interfacciamento con l'interfaccia grafica
    """

    @single_conn
    def leggi_stato(self):
        #cmd = CMD_GETSTATUS % self.io.config.APl
        cmd = OpenMSG.build_status_request('1', self.io.config.APl)
        self._invia(cmd)
        #data = self._ricevi()
        #data = data.split('*')
        # ['', '1', '0', '21##']
        #return int(data[2])
        msg = self._recv_msg()
        return 0

    @single_conn
    def aumenta_luce(self):
        cmd = CMD_MORE % self.io.config.APl
        self._invia(cmd)
        self._leggi_ack()

    @single_conn
    def riduci_luce(self):
        cmd = CMD_LESS % self.io.config.APl
        self._invia(cmd)
        self._leggi_ack()

    @single_conn
    def accendi(self):
        cmd = CMD_ON % self.io.config.APl
        self._invia(cmd)
        self._leggi_ack()

    @single_conn
    def spegni(self):
        cmd = CMD_OFF % self.io.config.APl
        self._invia(cmd)
        self._leggi_ack()

    """
    """

    def _recv_msg(self):
        buf, param = '', False
        while True:
            try:
                c = self._s.recv(1)
            except socket.error:
                log.exception('')
                self._disconnetti()
                raise
            else:
                buf += c
                if c == '#':
                    if param:
                        # doppio "#"
                        break
                    else:
                        # singolo "#", potrebbe esserci un parametro
                        param = True
                else:
                    # resetto contatore "#"
                    param = False
        log.debug('ricevuto %s' %buf)
        msg = OpenMSG(buf)
        return msg

    def _connetti(self):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.connect((self.io.config.Ip, self.io.config.Porta))
        self._leggi_ack()

    def _disconnetti(self):
        if self._s:
            self._s.close()
        self._s = None

    def _leggi_ack(self):
        #ack = self._ricevi(len(CMD_ACK))
        msg = self._recv_msg()
        if msg.is_nack:
            log.error('ricevuto NACK')
        elif msg.is_ack:
            log.debug('ricevuto ACK')
        else:
            log.error('atteso ack/nack, trovato %s' %msg)

    def _invia(self, data):
        try:
            log.debug('invio %s' %data)
            sent = self._s.send(str(data))
        except socket.error:
            log.exception('inviando %s' %data)

    def _ricevi(self, maxb=1024):
        try:
            data = self._s.recv(maxb)
        except socket.error:
            log.exception('ricevendo %s' %maxb)
            # raise
            return ''
        else:
            log.debug('ricevo %s' %data)
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

