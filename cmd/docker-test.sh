#!/bin/bash
export PROJECTNAME=AI-Chat-Bot-IFSGuide_service
export NETWORKNAME=AI-Chat-Bot-IFSGuide_service_network
export HOSTNAME=AI-Chat-Bot-IFSGuide_service
export PORT=6601
docker run --rm -it \
      --name $PROJECTNAME \
      -p $PORT:6601 \
      -v ./:/app \
      --network $NETWORKNAME \
      --hostname $HOSTNAME \
      AI-Chat-Bot-IFSGuide_service:latest