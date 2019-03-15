#!/bin/bash
if [ "SYNCRONIZE" = "true" ]
    then
        MAX_CONN=100
    else
        MAX_CONN=0
fi
envsubst  < /root/template.zcash.conf | dd of=/root/.zcash/zcash.conf
zcashd