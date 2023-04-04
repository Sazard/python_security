docker stop python-securite;
docker rm python-securite;
docker build -t python-securite:dev .;
docker run -v "$PWD/:/opt/python-securite" --name python-securite -it python-securite:dev;