#!/usr/bin/env bash
set -e

if [ ! -f .env ]; then
  cat > .env <<'EOF'
TELEGRAM_TOKEN=
OPENAI_API_KEY=
OWNER_ID=2342342
EOF
fi
