#!/bin/bash

source .env

if [ $keep_data_in_ram = "true" ]
    then
        echo "zcashd_volume_type=tmpfs" >> .env
    else
        echo "zcashd_volume_type=volume" >> .env
fi

if [ $persist_data = "true" ]
    then
        echo "zcashd_volume_type=volume" >> .env
fi

if [ -z "$zcash_data_dir" ]
    then
        echo "zcashd_volume_source=vol-zcashd" >> .env
    else
        echo "zcashd_volume_type=bind" >> .env
        echo "zcashd_volume_source=$zcash_data_dir" >> .env