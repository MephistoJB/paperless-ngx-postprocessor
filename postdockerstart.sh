#!/bin/bash

# Check if postdockerstart.sh already exists
if [ -f "/etc/init.d/postdockerstart.sh" ]; then
    echo "postdockerstart.sh already exists, removing PAPERLESS_PRE_CONSUME_SCRIPT and exiting"
    unset PAPERLESS_PRE_CONSUME_SCRIPT
    exit 0
fi

ln -s  /usr/src/paperless/paperless-ngx_postprocessor/postdockerstart.sh /etc/init.d/postdockerstart.sh
apt update
apt install cron nano procps -y
/usr/src/paperless/scripts/setup_venv.sh
printenv >> /etc/environment
crontab -u root /usr/src/paperless/paperless-ngx_postprocessor/cronjob
#cron -f
cron
