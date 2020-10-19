FROM debian:bullseye

WORKDIR /root

COPY plot.py .

RUN apt update
RUN apt -y install python3

# CMD ./plot.py
