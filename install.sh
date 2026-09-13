#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
USER_NAME="$(id -un)"
SERVICE_NAME="httpinspector"

sudo apt update
sudo apt install -y python3 python3-venv python3-pip

cd "$ROOT"
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/pip install mitmproxy

if [[ ! -f config.env ]]; then
  cp config.env.example config.env
  echo "Created $ROOT/config.env with the default Inspector endpoint and port."
fi

sudo tee "/etc/systemd/system/${SERVICE_NAME}.service" >/dev/null <<EOF
[Unit]
Description=HTTP Inspector mitmproxy service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${USER_NAME}
WorkingDirectory=${ROOT}
Environment=HOME=${HOME}
ExecStart=/bin/bash ${ROOT}/start.sh
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

echo
echo "Installation complete."
echo "Inspector UI: https://daulac.nomzom.lol/http-inspector/"
echo "Proxy listener: 0.0.0.0:8445"
echo "Status: sudo systemctl status $SERVICE_NAME"
echo "Logs: journalctl -u $SERVICE_NAME -f"
