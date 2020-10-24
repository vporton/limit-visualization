FROM debian:bullseye

WORKDIR /root

COPY plot.py .

RUN apt update
RUN apt -y install python3 python3-numpy python3-pip
RUN pip3 install matplotlib==3.3.2

WORKDIR /golem/work

VOLUME /golem/work

CMD tail -f /dev/null