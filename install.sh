#!/bin/bash

btc_blocks_dir=/opt/platform/bitcoin-data/blocks
database_dir=/opt/platform/mongo-data
mongo_max_memory=10000   # in Mb

if [ $btc_blocks_dir == "not_set" ]
    then echo "please set btc_blocks_dir variable, it should contain absolute path to directory containing bitcoin blkXXXXX.dat files"
    exit
fi

if [ $database_dir == "not_set" ]
    then echo "please set database_dir variable, it should contain absolute path to directory in witch you want to keep your database"
    exit
fi

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

./uninstall.sh  # this should not be in production



docker network create btcnet

docker build -t btc-blockchain-db ./database

docker run -d --network=btcnet --name btc-blockchain-db -v $database_dir:/data/db btc-blockchain-db --memory=$mongo_max_memory

docker build -t btc-blockchain-db-maintainer ./database-maintainer

docker run -d --network=btcnet --name btc-blockchain-db-maintainer -v $btc_blocks_dir:/btc-blocks-data btc-blockchain-db-maintainer

docker build -t btc-blockchain-web-api ./web-api

docker run -d --network=btcnet --name btc-blockchain-web-api -p 80:80 btc-blockchain-web-api




