#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ln -s "$DIR/postdockerstart.sh" /etc/init.d/postdockerstart.sh
apt update
apt install cron nano procps -y
"$DIR/setup_venv.sh"

printenv >> /etc/environment
crontab -u root "$DIR/cronjob"
#cron -f
cron

# Append local_runner_service start to /init so it runs at the end of container init
if [ -f "/init" ] && [ -w "/init" ]; then
    if ! grep -q "local_runner_service.py" /init 2>/dev/null; then
        cat >>/init <<EOF

# Start local_runner_service (appended by postdockerstart.sh)
(
  if ! pgrep -f "local_runner_service.py" >/dev/null 2>&1; then
    PY_BIN="python3"
    DIR="$DIR"
    if [ -x "$DIR/venv/bin/python3" ]; then
      PY_BIN="$DIR/venv/bin/python3"
    fi
    nohup "$PY_BIN" "$DIR/local_runner_service.py" >>/var/log/local_runner_service.log 2>&1 &
  fi
) &
EOF
        chmod +x /init
    fi
fi
