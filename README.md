# Claude Code Statusline

A 3-line statusline for [Claude Code](https://claude.ai/code) with true-colour ANSI, Nerd Font glyphs, and system stats.

Colours from the [if_tea](https://github.com/JanDeDobbeleer/oh-my-posh) oh-my-posh theme.

## Preview

![Claude Code statusline preview](statusline-preview.jpg)

## Variants

| Variant | OS | Runtime | Shell |
|---|---|---|---|
| [`ubuntu-fish/`](ubuntu-fish/) | Ubuntu / WSL | Python 3.6+ | fish / bash |
| [`windows-omp/`](windows-omp/) | Windows | Node.js | PowerShell / Git Bash |

## Layout

**Line 1:** Model → CPU% │ RAM → session elapsed → shell → current directory

**Line 2:** Cost → time → day

**Line 3:** Context window usage bar → session usage bar → time until rate limit reset

## Requirements

- [Claude Code](https://claude.ai/code)
- A [Nerd Font](https://www.nerdfonts.com/) in your terminal (e.g. MesloLGS NF, FiraCode NF)
- See variant subfolder for runtime requirements

## Install

See `SETUP.md` in the relevant subfolder:
- [ubuntu-fish/SETUP.md](ubuntu-fish/SETUP.md)
- [windows-omp/SETUP.md](windows-omp/SETUP.md)

## License

GNU General Public License v3.0
