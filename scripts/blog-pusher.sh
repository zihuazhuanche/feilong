#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "用法: scripts/blog-pusher.sh <url> [extra args...]"
  exit 1
fi

REPO_ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$REPO_ROOT"

python3 scripts/blog-pusher.py "$@" --build --commit ${PUSH:+--push}
