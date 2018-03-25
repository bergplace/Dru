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

source ./startup-scripts/install_db
source ./startup-scripts/install_db_maintainer
source ./startup-scripts/install_web_api


