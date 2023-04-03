FROM ubuntu:latest

WORKDIR /opt/python-securite

RUN \
  apt-get update && \
  apt-get -y install python3 python3-pip iputils-ping && \
  pip3 install scapy

USER root

CMD ["python3","src/main.py","-1", "192.168.1.199"]