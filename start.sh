#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f config.env ]]; then
  echo "Missing config.env. Copy config.env.example to config.env and set INSPECTOR_ENDPOINT."
  exit 1
fi

set -a
source ./config.env
set +a

: "${INSPECTOR_ENDPOINT:?INSPECTOR_ENDPOINT is required}"
LISTEN_HOST="${LISTEN_HOST:-0.0.0.0}"
LISTEN_PORT="${LISTEN_PORT:-8445}"

exec ./.venv/bin/mitmdump \
  --listen-host "$LISTEN_HOST" \
  --listen-port "$LISTEN_PORT" \
  --set block_global=false \
  -s ./inspector.py
