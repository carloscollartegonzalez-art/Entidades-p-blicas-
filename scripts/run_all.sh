#!/usr/bin/env bash
# Atajo para macOS/Linux; en Windows usa:  python scripts/run_all.py
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/run_all.py
