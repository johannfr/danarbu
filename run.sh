#!/bin/bash

app="danarbu"

for docker_id in $(docker ps -a | grep ${app} | awk '{print $1}')
do
    docker stop ${docker_id}
    docker rm ${docker_id}
done

docker build -t ${app}:latest -f docker/Dockerfile .
docker run -d -p 80:80 \
    --name=${app} \
    --network="host" \
    -e FLASK_APP=main.py \
    -e DANARBU_DBURI="" \
    -v ${PWD}:/app ${app}
