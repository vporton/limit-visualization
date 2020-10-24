#!/usr/bin/make -f

.PHONY: all docker test-docker

all: .image.hash
	yagna payment init -r
	./script.py

docker:
	docker build -t limit-visualization .

test-docker: docker
	CONTAINER=`docker run -d limit-visualization`; \
		docker start $$CONTAINER; \
		docker exec $$CONTAINER /root/plot.py 0; \
		docker stop $$CONTAINER; \
		docker container rm $$CONTAINER

.image.hash: docker
	gvmkit-build limit-visualization --push | perl -ne 'print $$1 if /hash link (.*)/' > $@
