#!/bin/bash

source .env

if [ $keep_data_in_ram = "true" ]
    then
        echo "zcashd_volume_type=tmpfs" >> .env
        echo "mongo_volume_type=tmpfs" >> .env
    else
        echo "zcashd_volume_type=volume" >> .env
        echo "mongo_volume_type=volume" >> .env
fi

if [ $persist_data = "true" ]
    then
        echo "zcashd_volume_type=volume" >> .env
        echo "mongo_volume_type=volume" >> .env
fi

if [ -z "$zcash_dir" ]
    then
        echo "zcashd_volume_source=vol-zcashd" >> .env
    else
        echo "zcashd_volume_type=bind" >> .env
        echo "zcashd_volume_source=$zcash_dir" >> .env
fi

if [ -z "$mongo_dir" ]
    then
        echo "mongo_volume_source=vol-mongo" >> .env
    else
        echo "mongo_volume_type=bind" >> .env
        echo "mongo_volume_source=$mongo_dir" >> .env
fi