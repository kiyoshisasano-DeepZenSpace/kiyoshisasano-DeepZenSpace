#!/usr/bin/env bash
# Quick validator wrapper (optional)
set -euo pipefail
if ! command -v python >/dev/null 2>&1; then
  echo "python is required"; exit 1
fi
python bootstrap_demo.py
