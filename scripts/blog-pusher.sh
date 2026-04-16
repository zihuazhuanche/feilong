#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "用法: scripts/blog-pusher.sh <url> [extra args...]"
  echo "可选: PUSH=1 并通过环境变量提供 GITHUB_TOKEN 或 GH_TOKEN"
  exit 1
fi

REPO_ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$REPO_ROOT"

if [ -n "${PUSH:-}" ] && [ -z "${GITHUB_TOKEN:-}${GH_TOKEN:-}" ]; then
  echo "PUSH=1 时必须通过环境变量提供 GITHUB_TOKEN 或 GH_TOKEN" >&2
  exit 2
fi

args=("$@" --build --commit)
if [ -n "${PUSH:-}" ]; then
  args+=(--push)
fi

python3 scripts/blog-pusher.py "${args[@]}"
