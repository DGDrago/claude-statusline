#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
input=$(cat)
printf '%s' "$input" > "$SCRIPT_DIR/statusline_debug.json" 2>/dev/null || true
printf '%s' "$input" | node "$SCRIPT_DIR/statusline.js" 2>/dev/null \
  || printf " Claude \n░░░░░░░░░░░░░░░░░░░░ --%%  | \$0.000 | 0m 0s\n"
