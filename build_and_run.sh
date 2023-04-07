#!/bin/bash

docker-compose -f "$PWD/tests/docker-compose.yml" down ;
docker-compose -f "$PWD/tests/docker-compose.yml" up -d ;
docker stop python-securite ;
docker rm python-securite ;
docker build -t python-securite:dev . ;
docker run -v "$PWD/:/opt/python-securite" --name python-securite -it --ip 172.18.1.10 --network test_network python-securite:dev ;