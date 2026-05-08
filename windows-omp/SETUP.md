# Claude Code Statusline — Windows / Oh My Posh variant

Requires: Node.js, Nerd Font (e.g. FiraCode Nerd Font, JetBrainsMono NF), Git Bash or WSL

## Install

### 1. Copy files

```bash
cp statusline.js ~/.claude/
cp statusline-command.sh ~/.claude/
```

On Windows: `C:\Users\<you>\.claude\`

### 2. Add to Claude Code settings

`~/.claude/settings.json` (or `C:\Users\<you>\.claude\settings.json`):

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash C:/Users/<you>/.claude/statusline-command.sh"
  }
}
```

## Layout

**Line 1:** Model → CPU% │ RAM → session elapsed → shell → current directory

**Line 2:** Cost → time → day

**Line 3:** Context window usage bar → session usage bar → time until rate limit reset

## Colors

Palette from [if_tea oh-my-posh theme](https://github.com/JanDeDobbeleer/oh-my-posh):

| Segment | bg | fg |
|---|---|---|
| Model | `#1865f5` | `#ffffff` |
| CPU/RAM | `#00c7fc` | `#000000` |
| Exec time | `#2343e2` | `#ffffff` |
| Shell | `#91f2ff` | `#000000` |
| Cost/Time/Day | `#ff8c94` | `#000000` |
| Dir/Path | `#f8677b` | `#000000` |
