# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\unpackTK.py'), os.path.join(HOMEPATH,'support\\useTK.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'illuminator.py', os.path.join(HOMEPATH,'support\\removeTK.py')],
#             pathex=['E:\\myels'])
)
pyz = PYZ(a.pure)

# aggiungere i file dati
a.datas += [('icon.xbm', 'icon.xbm', 'DATA'),
	    ('logo.gif', 'logo.gif', 'DATA')]

exe = EXE(TkPKG(), pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'illuminator_dev.exe'),
          debug=True,
          strip=False,
          upx=True,
          console=True,
          icon='icon.ico')
app = BUNDLE(exe,
             name=os.path.join('dist', 'illuminator.exe.app'))
