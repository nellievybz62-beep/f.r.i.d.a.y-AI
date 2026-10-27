#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

node -e 'if (+process.versions.node.split(".")[0] < 20) {
  console.error("Node.js 20 or newer is required."); process.exit(1)
}'

if [ ! -f vendor/hmem/package.json ]; then
  TMP="$(mktemp -d)"
  trap 'rm -rf "$TMP"' EXIT

  if [ -n "${METERLESS_REPO_PATH:-}" ] &&
     [ -f "$METERLESS_REPO_PATH/engines/hmem/reference/package.json" ]; then
    ENGINE="$METERLESS_REPO_PATH/engines/hmem/reference"
  else
    git clone --depth 1 https://github.com/Meterless/Meterless.git "$TMP/source"
    ENGINE="$TMP/source/engines/hmem/reference"
  fi

  mkdir -p vendor
  cp -a "$ENGINE" vendor/hmem
fi

cd vendor/hmem
npm install --no-audit --no-fund
