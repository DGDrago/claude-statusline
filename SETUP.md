# Claude Code Statusline — Setup Instructions

Requires: Node.js, Nerd Font (e.g. FiraCode Nerd Font, JetBrainsMono NF)

## Install

### 1. Copy files
```
~/.claude/statusline.js
~/.claude/statusline-command.sh
```

On **Windows**: `C:\Users\<you>\.claude\`
On **Mac/Linux**: `~/.claude/`

### 2. Make script executable (Mac/Linux)
```bash
chmod +x ~/.claude/statusline-command.sh
```

### 3. Add to Claude Code settings
File: `~/.claude/settings.json`
```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/statusline-command.sh"
  }
}
```

On **Windows** (Git Bash / WSL):
```json
{
  "statusLine": {
    "type": "command",
    "command": "bash C:/Users/<you>/.claude/statusline-command.sh"
  }
}
```

## Layout

```
[Sonnet 4.6][CPU: 12% | RAM: 14.2/31.9GB][⧖ 5m 12s][pwsh][📁 ~/projects]
 [$0.042 | © 02:15:30 PM | Thursday 📅]
 [ctx ████████░░░░] [sess ███░░░░░░░░░] ⧖ 2h 45m
```

## Colors
Palette from oh-my-posh `if_tea.omp.json` theme.
Nerd Font diamond glyphs (requires Nerd Font in terminal).
