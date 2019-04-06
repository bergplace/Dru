#!/bin/bash

source .env

if [ $use_docker_zcash_node = "true" ]
    then
        ZCASH_NODES=1
    else
        ZCASH_NODES=0
fi

docker-compose up -V --scale zcashd=$ZCASH_NODES
