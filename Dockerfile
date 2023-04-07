FROM debian:stable

WORKDIR /opt/python-securite

RUN \
  apt-get update && \
  apt-get -y install python3 python3-pip iputils-ping nmap iproute2

COPY requirements.txt .

RUN \
  pip install -r requirements.txt

USER root

# CMD ["bash","tests/run_tests.sh"]
