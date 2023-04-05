FROM debian:stable

WORKDIR /opt/python-securite

RUN \
  apt-get update && \
  apt-get -y install python3 python3-pip iputils-ping && \
  pip3 install scapy pytest python-nmap

USER root

CMD ["bash","tests/run_tests.sh"]
