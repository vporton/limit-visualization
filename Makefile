#!/usr/bin/make -f

.PHONY: all docker test-docker

.PRECIOUS: .image.hash

all: continuous.gif discontinuous.gif

continuous.gif: .image.hash
	yagna payment init -r
	./script.py

discontinuous.gif: .image.hash
	yagna payment init -r
	./script2.py

docker:
	docker build -t limit-visualization .

test-docker: docker
	CONTAINER=`docker run -d limit-visualization`; \
		docker start $$CONTAINER; \
		docker exec $$CONTAINER /root/plot.py 0; \
		docker stop $$CONTAINER; \
		docker container rm $$CONTAINER

.image.hash: docker
	HASH=`gvmkit-build limit-visualization --push | perl -ne 'print $$1 if /hash link (.*)/'`; \
		test "$$HASH" != ""; \
		echo -n $$HASH > $@
