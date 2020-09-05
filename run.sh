#!/bin/bash

app="danarbu"
docker build -t ${app}:latest -f docker/Dockerfile .
docker run -d -p 56733:80 \
    --name=${app} \
    -v ${PWD}:/app ${app}
