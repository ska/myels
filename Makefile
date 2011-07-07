#
# installare cygwin con i pacchetti wget, make
#

NAME=illuminator
CONFIG=config.mk
PYINST_VER=1.5
PYINST_DIR=pyinstaller-$(PYINST_VER)
PYINST_FILE=$(PYINST_DIR).tar.bz2

.PHONY: all config
all: build_pyinst


#$(CONFIG):
#	#echo Genero file di configurazione..;
#	echo PYINST_DIR=pyinstaller-1.5 >> $(CONFIG); \
#	echo version=$(shell python -c "import illuminator; print illuminator.version") >> $(CONFIG); \
#	echo Fatto;
#	#@echo PYINST_DIR=$(shell find / -name pyinstaller-$(PYINST_VER) -type d -print0 2>/dev/null) >> $(CONFIG)
#
#config: $(CONFIG)
#
#HAHAHA=$(shell ls $(CONFIG) 2>/dev/null)x
#ifneq ($(shell ls $(CONFIG) 2>/dev/null)x, x)
#	include $(CONFIG)
#endif
##include $(CONFIG)
#ifeq ($(PYINST_DIR),'')
#	@echo Pyinstaller manca! eseguire make download_pyinst
#endif



.PHONY: download_pyinst pyinstaller
download_pyinst:
	# genera template del file .spec per costruire l'exe
	wget http://www.pyinstaller.org/static/source/$(PYINST_VER)/$(PYINST_FILE)
	tar xjf $(PYINST_FILE)
	rm -f $(PYINST_FILE)
	python $(PYINST_DIR)/Configure.py

pyinstaller: $(PYINST_DIR)

$(NAME).spec: pyinstaller
	#python $(PYINST_DIR)/Makespec.py --onefile --tk --windowed --debug --name $(NAME) $(NAME).py

build_pyinst: $(NAME).spec
	python $(PYINST_DIR)/Build.py $(NAME).spec

#build_py2exe:
#	python setup.py py2exe

build_cxfreeze:
	python setup.py build

#all: build_py2exe
#all: build_cxfreeze



.PHONY: clean
clean:
	rm -vf .*.sw[op] *.pyc

.PHONY: distclean
distclean: clean
	rm -rvf build/ dist/ $(CONFIG)


