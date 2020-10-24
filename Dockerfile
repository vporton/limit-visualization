FROM debian:bullseye

WORKDIR /root

COPY plot.py .

RUN apt update
RUN apt -y install python3

WORKDIR /golem/work

VOLUME /golem/work
