#!/bin/bash
export PROJECTNAME=ai_chat_bot_service
export NETWORKNAME=ai_chat_bot_service_network
export HOSTNAME=ai_chat_bot_service
export PORT=6601
docker run --rm -it \
      --name $PROJECTNAME \
      -p $PORT:6601 \
      -v ./:/app \
      --network $NETWORKNAME \
      --hostname $HOSTNAME \
      ai_chat_bot_service:latest