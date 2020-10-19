#!/usr/bin/make -f

.PHONY: all

all:
	docker build -t limit-visualization .
	gvmkit-build limit-visualization
	yagna payment init -r
	./script.py
