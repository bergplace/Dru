#!/bin/bash

source .env

if [ $use_docker_zcash_node = "true" ]
    then
        ZCASH_NODES=1
    else
        ZCASH_NODES=0
fi

if [ $debug = "true" ]
    then
        MONGO_EXPRESS=1
    else
        MONGO_EXPRESS=0
fi

docker compose up -V --scale zcashd=$ZCASH_NODES --scale mongo-express=$MONGO_EXPRESS $1
