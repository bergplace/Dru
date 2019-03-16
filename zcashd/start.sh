#!/bin/bash
if [ $TEST_MODE = "false" ]
    then
        export MAX_CONN=100
    else
        export MAX_CONN=0
        echo "reindex=1" >> /root/template.zcash.conf
fi
envsubst  < /root/template.zcash.conf | dd of=/root/.zcash/zcash.conf
zcashd