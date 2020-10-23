#!/usr/bin/make -f

.PHONY: all

all: .image.hash
#	yagna payment init -r
	./script.py

.image.hash:
	docker build -t limit-visualization .
	gvmkit-build limit-visualization --push | perl -ne 'print $$1 if /hash link (.*)/' > $@
