#!/bin/bash
# Este pequeño script permite desplegar un contenedor para desarrollo
# o para producción.
# Sintaxis:
# ./start.sh dev   para desplegar el contenedor en modo desarrollo
# ./start.sh para desplegar el contenedor en modo producción/pruebas

if [ "$1" == "dev" ];
then
  cp Dockerfile-dev Dockerfile
  sudo docker build -t tpaga-test-backend:latest ./
  sudo docker run --rm --name tpaga-test-backend -p 8000:8000 -v "$(pwd)"/tpaga/:/opt/app/tpaga tpaga-test-backend:latest
else
  cp Dockerfile-prod Dockerfile
  sudo docker build -t tpaga-test-backend:latest ./
  sudo docker run --rm --name tpaga-test-backend -p 8000:8000 tpaga-test-backend:latest
fi
