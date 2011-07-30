
import os
import logging
import ConfigParser

log = logging.getLogger('config')

class Config:
    default = {'APl':'11',
               'Ip':'192.168.1.35',
               'Porta':'20000'
              }
    def __init__(self, io):
        self.io = io
        self.version= '0.99b'
        self.__configured = False

        # il file di configurazione va settato nascosto,
        # su win il file deve esistere per cui viene reso nascosto
        # al momento della creazione in write_config
        if os.name == "posix":
            self.config_file = os.path.join(os.environ['HOME'], ".illuminator")
        elif os.name == "nt":
            self.config_file = os.path.join(os.environ['USERPROFILE'], "illuminator")
        else:
            self.config_file = os.tmpnam()

    def check_config(self):
        if os.path.exists(self.config_file):
            self.read_config()
            return True
        else:
            self.io.finestra.leggiConfig()
            return False

    def write_config(self, vals):
        d = self.default.copy()
        d.update(vals)
        cp = ConfigParser.SafeConfigParser()
        cp.add_section('luce')
        for k, v in d.items():
            cp.set('luce', k, v)
        with open(self.config_file, 'wt+') as fh:
            try:
                if os.name == 'nt':
                    import win32api, win32con
                    win32api.SetFileAttributes(self.config_file, win32con.FILE_ATTRIBUTE_HIDDEN)
                cp.write(fh)
            except:
                log.exception('Scrivendo %s' %self.config_file)

    def read_config(self):
        with open(self.config_file, 'rt') as fh:
            cp = ConfigParser.SafeConfigParser(defaults=self.default)
            try:
                log.debug('leggo da %s' %self.config_file)
                cp.readfp(fh)
                self.APl = cp.get('luce', 'APl')
                self.Ip = cp.get('luce', 'Ip')
                self.Porta = cp.getint('luce', 'Porta')
            except ConfigParser.Error:
                log.exception('Leggendo %s' %self.config_file)

