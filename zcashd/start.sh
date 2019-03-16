#!/bin/bash
if [ $TEST_MODE = "false" ]
    then
        export MAX_CONN=100
        export REINDEX=0
    else
        export MAX_CONN=0
        export REINDEX=1
fi
envsubst  < /root/template.zcash.conf | dd of=/root/.zcash/zcash.conf
zcashd