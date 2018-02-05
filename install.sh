#!/bin/bash

btc_blocks_dir=/home/marcin/nfs
database_dir=/home/marcin/btc_mongo

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

docker build -t btc-blockchain-db ./database

docker run -d --name btc-blockchain-db -v $database_dir:/data/db btc-blockchain-db

docker build -t btc-blockchain-db-maintainer ./database-maintainer

docker run -d --name btc-blockchain-db-maintainer -v $btc_blocks_dir:/btc-blocks-data --link btc-blockchain-db btc-blockchain-db-maintainer

