#!/usr/bin/env python
#
# apt-get install python-dev
# wget http://prdownloads.sourceforge.net/cx-freeze/cx_Freeze-4.2.3.tar.gz?download -O cx_Freeze-4.2.3.tar.gz
# tar xzf cx_Freeze-4.2.3.tar.gz && cd cx_Freeze-4.2.3
# python setup.py install
#

### py2exe
import sys
#from distutils.core import setup
#
#import py2exe
#opt = {"py2exe": {"packages": ["encodings"], 'bundle_files':1}}
#
#sys.argv.append('py2exe')
#setup(options = opt, windows = [{"script": 'illuminator.py'}], zipfile=None)
##setup(console=['illuminator.py'])

## cx_Freeze
import sys
#from cx_Freeze import setup, Executable
#
#base = None
#if sys.platform == "win32":
#        base = "Win32GUI"
#
#setup(name='Illuminator',
#      version='0.1',
#      description='desc',
#      executables=[Executable(script = 'illuminator.py',
#                              base = base,
#                              icon = None,
#                              compress = True,
#                              copyDependentFiles = True,
#                              appendScriptToLibrary = True)]
#      )


## distutils
import bbfreeze
#from distutils.core import setup
from setuptools import setup, find_packages

from distutils import log
log.set_verbosity(20)

setup(name='Illuminator',
      version='1.0',
      description='Ilululumin',
      author='BrikSkag',
      author_email='poseidone',
      url='http://',
      #packages=['illuminator'],
      packages = find_packages(),
      verbose=20,
      #scripts=['illuminator.py']
      entry_points = {'gui_scripts':'illuminator = illuminator:main'},
      package_data={'':['*.ico']}
      )


