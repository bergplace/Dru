#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

source ./startup-scripts/uninstall_web_api
source ./startup-scripts/uninstall_db_maintainer
source ./startup-scripts/uninstall_db

docker network rm btcnet
