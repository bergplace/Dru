#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

docker stop btc-blockchain-db
docker rm btc-blockchain-db
docker stop btc-blockchain-db-maintainer
docker rm btc-blockchain-db-maintainer
docker network rm btcnet
