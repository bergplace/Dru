#!/bin/bash

source .env

if [ $use_docker_zcash_node = "true" ]
    then
        ZCASH_NODES=1
    else
        ZCASH_NODES=0
fi

if [ $persist_data = "true" ]
    then
        docker-compose up $* --scale zcashd=$ZCASH_NODES
    else
        docker-compose up -v $* --scale zcashd=$ZCASH_NODES
fi