#!/bin/bash
# Start Claude Code phone bridge on port 9090
# Usage: bash scripts/start_phone_claude.sh [port]

cd /Users/cyingfang/claude
python3 scripts/phone_claude_bridge.py "$@"
