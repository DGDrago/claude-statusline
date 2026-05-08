#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
input=$(cat)
printf '%s' "$input" > "$SCRIPT_DIR/statusline_debug.json" 2>/dev/null || true
printf '%s' "$input" | python3 "$SCRIPT_DIR/statusline.py" 2>/dev/null \
  || printf " Claude \n░░░░░░░░░░░░░░░░░░░░ --%%  | \$0.000 | 0m 0s\n"
