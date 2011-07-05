
#build_py2exe:
#	python setup.py py2exe

build_cxfreeze:
	python setup.py build

#all: build_py2exe
all: build_cxfreeze

clean:
	rm -vf .*.sw[op] *.pyc
	rm -rvf build/ dist/
