#!/bin/bash
envsubst  < /root/template.zcash.conf | dd of=/root/.zcash/zcash.conf
zcashd