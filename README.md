# Claude Code Statusline

A 3-line statusline for [Claude Code](https://claude.ai/code) in Ubuntu WSL terminal with true-colour ANSI, Nerd Font glyphs, and system stats.

## Preview

![Claude Code statusline preview](statusline-preview.jpg)

Colours from the [if_tea](https://github.com/JanDeDobbeleer/oh-my-posh) oh-my-posh theme.

## Requirements

- [Claude Code](https://claude.ai/code)
- Python 3.6+
- A [Nerd Font](https://www.nerdfonts.com/) in your terminal (e.g. MesloLGS NF, FiraCode NF)

## Install

### 1. Copy files

```bash
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

**Line 3:** Context window usage → session usage → time until rate limit reset

## License

GNU General Public License v3.0
