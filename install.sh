#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

docker build -t btc-blockchain-db-maintainer ./database-maintainer

read -p "Type in absolute path to the directory containing bitcoin blkXXXXX.dat files`echo $'\n> '`" btc_blocks_dir

docker run -v $btc_blocks_dir:/btc-blocks-data dbm

