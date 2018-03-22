#!/bin/bash

if (( $EUID == 0 )); then
    echo "Don't run as root, add your user to group 'docker' to run without sudo"
    exit
fi

if [ ! -f config.conf ]; then
    echo "file config.conf does not exist,"
    echo "you can create one from template_config.conf"
    exit
fi

source config.conf

if [ $btc_blocks_dir == "not_set" ] ||
   [ $database_dir == "not_set" ] ||
   [ $db_root_username == "not_set" ] ||
   [ $db_root_username == "not_set" ] ||
   [ $db_readonly_username == "not_set" ] ||
   [ $db_readonly_password == "not_set" ]
    then echo "please set variables in config.conf"
    exit
fi

docker network create btcnet

docker run -d \
    --name btc-blockchain-db \
    -e AUTH=yes \
    -e MONGODB_ADMIN_USER=$db_root_username \
    -e MONGODB_ADMIN_PASS=$db_root_password \
    -e MONGODB_APPLICATION_DATABASE=bitcoin \
    -p 0.0.0.0:$db_port:27017 \
    -v $database_dir:/data/db \
    --network=btcnet \
    aashreys/mongo-auth:latest


docker build -t btc-blockchain-db-maintainer ./database-maintainer

docker run -d \
    --name btc-blockchain-db-maintainer \
    -e MONGODB_ADMIN_USER=$db_root_username \
    -e MONGODB_ADMIN_PASS=$db_root_password \
    -e MONGODB_READONLY_USER=$db_readonly_username \
    -e MONGODB_READONLY_PASS=$db_readonly_password \
    -e TX_ADDRESS_CACHE_LIMIT=$tx_address_cache_limit \
    -v $btc_blocks_dir:/btc-blocks-data \
    --network=btcnet \
    btc-blockchain-db-maintainer

docker build -t btc-blockchain-web-api ./web-api

docker run -d \
    --name btc-blockchain-web-api \
    -e MONGODB_READONLY_USER=$db_readonly_username \
    -e MONGODB_READONLY_PASS=$db_readonly_password \
    -p 0.0.0.0:80:80 \
    --network=btcnet \
    btc-blockchain-web-api


