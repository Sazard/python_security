FROM ubuntu:latest

WORKDIR /opt/python-securite

RUN \
  apt-get update && \
  apt-get -y install python3 python3-pip && \
  python3 -m pip install --upgrade pip  && \
  pip3 install -r requirements.txt

USER root

CMD ["python3","src/main.py"]