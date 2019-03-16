#!/bin/bash

source .env

if [ $persist_data = "true" ]
    then
        docker-compose down
    else
        docker-compose down -v
fi