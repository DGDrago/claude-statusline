# Claude Code Statusline — Ubuntu / fish variant

Requires: Python 3.6+, Nerd Font (e.g. MesloLGS NF, FiraCode NF)

## Install

### 1. Copy files

```bash
cd ubuntu-fish/
cp statusline.py ~/.claude/
cp statusline-command.sh ~/.claude/
chmod +x ~/.claude/statusline.py ~/.claude/statusline-command.sh
```

### 2. Add to Claude Code settings

`~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/statusline-command.sh"
  }
}
```

## Layout

**Line 1:** Model → CPU% │ RAM → session elapsed → shell → current directory

**Line 2:** Cost → time → day

**Line 3:** Context window usage bar → session usage bar → time until rate limit reset
