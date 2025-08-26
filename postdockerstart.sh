#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
apt update
apt install cron nano procps -y
/usr/src/paperless-ngx-postprocessor/setup_venv.sh

printenv >> /etc/environment
crontab -u root "$DIR/cronjob"
#cron -f
cron


RUN_DIR="$DIR"
SERVICE_SCRIPT="$RUN_DIR/local_runner_service.py"

# Ensure log directory exists
mkdir -p /var/log

# Idempotently ensure /init runs the local runner in background at the end
# Remove previous managed block if present, then append a fresh one
if [ -f /init ]; then
  sed -i '/# BEGIN local_runner_service/,/# END local_runner_service/d' /init || true
else
  echo "#!/usr/bin/env bash" > /init
fi

if head -n 1 /init | grep -q '^#!'; then
  { head -n 1 /init; cat <<EOF; tail -n +2 /init; } > /init.new
# BEGIN local_runner_service
# Auto-managed by postdockerstart.sh - DO NOT EDIT BETWEEN MARKERS
nohup python3 "$SERVICE_SCRIPT" >> /var/log/local_runner_service.log 2>&1 &
# END local_runner_service
EOF
else
  { echo "#!/usr/bin/env bash"; cat <<EOF; cat /init; } > /init.new
# BEGIN local_runner_service
# Auto-managed by postdockerstart.sh - DO NOT EDIT BETWEEN MARKERS
nohup python3 "$SERVICE_SCRIPT" >> /var/log/local_runner_service.log 2>&1 &
# END local_runner_service
EOF
fi
mv /init.new /init

chmod +x /init
