#!/bin/bash

app="danarbu"

for docker_id in $(docker ps -a | grep ${app} | awk '{print $1}')
do
    docker stop ${docker_id}
    docker rm ${docker_id}
done

docker build -t ${app}:latest -f docker/Dockerfile .
# docker run -d --name ${app} -p 56733:80 \
#     -v $(pwd):/app \
#     -e FLASK_APP=main.py \
#     -e FLASK_DEBUG=1 ${app} bash -c "while true ; do sleep 10 ; done"

docker run -d -p 56733:80 \
    --name=${app} \
    -e FLASK_APP=main.py \
    -v ${PWD}:/app ${app}
