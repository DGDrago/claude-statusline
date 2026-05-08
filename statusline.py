#!/usr/bin/env python3
"""
statusline.py – Python 3 port of statusline.js for Claude Code status line.
Outputs 3 lines with ANSI true-colour + Nerd Font glyphs.
"""

import sys
import json
import os
import time
import datetime

# ── ANSI helpers ──────────────────────────────────────────────────────────────
R = '\x1b[0m'
B = '\x1b[1m'


def fg(hex_color: str) -> str:
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return f'\x1b[38;2;{r};{g};{b}m'


def bg(hex_color: str) -> str:
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return f'\x1b[48;2;{r};{g};{b}m'


# ── Palette (if_tea.omp.json) ─────────────────────────────────────────────────
C = {
    'bSysinfo':  '#00c7fc',
    'bExectime': '#2343e2',
    'bShell':    '#91f2ff',
    'bTime':     '#ff8c94',
    'bPath':     '#f8677b',
    'bModel':    '#1865f5',
    'fDark':     '#000000',
    'fWhite':    '#ffffff',
    'fStatus':   '#00BCF9',
    'fText':     '#91f2ff',
    'pGreen':    '#00dc53',
    'pYellow':   '#ffdc00',
    'pRed':      '#ff0000',
}

# ── Nerd Font glyphs ──────────────────────────────────────────────────────────
DL  = ''   # left rounded cap
DR  = ''   # right rounded cap
SEP = '\x1b[2m' + fg(C['fText']) + ' │ ' + R   # dimmed │


# ── System info: CPU via /proc/stat ──────────────────────────────────────────
def _read_cpu_stat():
    """Return (idle, total) from the first 'cpu' line of /proc/stat."""
    with open('/proc/stat', 'r') as f:
        line = f.readline()          # first line: 'cpu  ...'
    fields = line.split()[1:]        # drop 'cpu' label
    values = [int(x) for x in fields]
    # idle = idle + iowait (indices 3 and 4)
    idle  = values[3] + (values[4] if len(values) > 4 else 0)
    total = sum(values)
    return idle, total


def get_cpu_pct() -> int:
    idle1, total1 = _read_cpu_stat()
    time.sleep(0.1)
    idle2, total2 = _read_cpu_stat()
    diff_total = total2 - total1
    diff_idle  = idle2  - idle1
    if diff_total == 0:
        return 0
    return round((1 - diff_idle / diff_total) * 100)


# ── System info: RAM via /proc/meminfo ────────────────────────────────────────
def get_ram_gb():
    """Return (used_gb_str, total_gb_str)."""
    info = {}
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 2:
                info[parts[0].rstrip(':')] = int(parts[1])   # kB
    total_kb = info.get('MemTotal', 0)
    free_kb  = info.get('MemFree',  0)
    buffers  = info.get('Buffers',  0)
    cached   = info.get('Cached',   0)
    sreclaimable = info.get('SReclaimable', 0)
    used_kb  = total_kb - free_kb - buffers - cached - sreclaimable
    used_gb  = used_kb  / 1_048_576
    total_gb = total_kb / 1_048_576
    return f'{used_gb:.1f}', f'{total_gb:.1f}'


# ── Session timer ─────────────────────────────────────────────────────────────
def get_elapsed_str(sid: str) -> str:
    if not sid:
        return '0m 0s'
    ts_file = f'/tmp/claude_session_start_{sid}'
    start_ts = None
    try:
        with open(ts_file, 'r') as f:
            start_ts = int(f.read().strip())
    except Exception:
        pass
    now_ts = int(time.time())
    if not start_ts:
        start_ts = now_ts
        try:
            with open(ts_file, 'w') as f:
                f.write(str(start_ts))
        except Exception:
            pass
    elapsed = max(0, now_ts - start_ts)
    mins = elapsed // 60
    secs = elapsed % 60
    return f'{mins}m {secs}s'


# ── Progress bar ──────────────────────────────────────────────────────────────
def progress_bar_styled(pct: int, label: str) -> str:
    EXTRA      = 12
    extra_blue = round(pct * EXTRA / 100)
    extra_cyan = EXTRA - extra_blue
    return (
        bg(C['bModel'])   + fg(C['fDark']) + ' ' + label + ' ' + ' ' * extra_blue + R
      + bg(C['bSysinfo']) + fg(C['fDark']) + ' ' * extra_cyan + ' ' + str(pct) + '% used ' + R
    )


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    raw = sys.stdin.read()
    try:
        d = json.loads(raw)
    except Exception:
        d = {}

    # Model name
    model = d.get('model', {})
    if isinstance(model, dict):
        model_name = model.get('display_name') or model.get('id') or 'Claude'
    else:
        model_name = str(model) if model else 'Claude'
    model_name = model_name.removeprefix('Claude ').removeprefix('claude-')

    # Directory
    cwd  = d.get('cwd', '')
    home = os.environ.get('HOME') or os.environ.get('USERPROFILE') or ''
    if home and cwd.startswith(home):
        display_dir = '~' + cwd[len(home):].replace('\\', '/')
    else:
        display_dir = cwd or '~'

    # Context window
    ctx      = d.get('context_window', {}) or {}
    used_pct = ctx.get('used_percentage')
    used_pct = round(used_pct) if used_pct is not None else None

    # Cost
    cost_usd = float((d.get('cost') or {}).get('total_cost_usd', 0) or 0)
    cost_str = f'{cost_usd:.3f}'

    # Session timer
    sid         = d.get('session_id', '')
    elapsed_str = get_elapsed_str(sid)

    # Rate limits
    rl       = d.get('rate_limits', {}) or {}
    sess_rl  = rl.get('five_hour') or rl.get('session') or {}
    sess_used_raw = sess_rl.get('used_percentage')
    sess_used = round(sess_used_raw) if sess_used_raw is not None else None

    reset_str = None
    resets_at = sess_rl.get('resets_at')
    if resets_at:
        if isinstance(resets_at, (int, float)):
            ts_ms = resets_at * 1000
        else:
            ts_ms = datetime.datetime.fromisoformat(str(resets_at)).timestamp() * 1000
        diff_ms = ts_ms - time.time() * 1000
        if diff_ms > 0:
            s = int(diff_ms / 1000)
            h = s // 3600
            m = (s % 3600) // 60
            reset_str = f'{h}h {m}m' if h > 0 else f'{m}m {s % 60}s'
        else:
            reset_str = 'now'

    # System stats
    cpu_pct          = get_cpu_pct()
    ram_used, ram_total = get_ram_gb()

    # Time / day
    now      = datetime.datetime.now()
    time_str = now.strftime('%I:%M:%S %p')   # e.g. 03:45:02 PM
    day_str  = now.strftime('%A')             # e.g. Thursday

    # Shell
    shell_path = os.environ.get('SHELL') or os.environ.get('ComSpec') or 'bash'
    shell = os.path.basename(shell_path).replace('.exe', '')

    # ── LINE 1 ────────────────────────────────────────────────────────────────
    line1 = ''
    line1 += fg(C['bModel']) + DL + R
    line1 += bg(C['bModel']) + fg(C['fWhite']) + B + ' ' + model_name + ' ' + R
    line1 += fg(C['bModel']) + bg(C['bSysinfo']) + DR + R
    line1 += bg(C['bSysinfo']) + fg(C['fDark']) + B + f' CPU: {cpu_pct}% │ RAM: {ram_used}/{ram_total}GB ' + R
    line1 += fg(C['bSysinfo']) + bg(C['bExectime']) + DR + R
    line1 += bg(C['bExectime']) + fg(C['fWhite']) + B + ' ⧖ ' + elapsed_str + ' ' + R
    line1 += fg(C['bExectime']) + bg(C['bShell']) + DR + R
    line1 += bg(C['bShell']) + fg(C['fDark']) + B + ' ' + shell + ' ' + R
    line1 += fg(C['bShell']) + bg(C['bPath']) + DR + R
    line1 += bg(C['bPath']) + fg(C['fDark']) + B + ' \U0001f4c1 ' + display_dir + ' ' + R
    line1 += fg(C['bPath']) + DR + R
    sys.stdout.write(line1 + '\n')

    # ── LINE 2 ────────────────────────────────────────────────────────────────
    line2 = ' '
    line2 += fg(C['bTime']) + DL + R
    line2 += bg(C['bTime']) + fg(C['fDark']) + B + f' ${cost_str} │ © {time_str} │ {day_str} \U0001f4c5 ' + R
    line2 += fg(C['bTime']) + DR + R
    sys.stdout.write(line2 + '\n')

    # ── LINE 3 ────────────────────────────────────────────────────────────────
    line3 = ' '
    line3 += fg(C['bModel']) + DL + R
    if used_pct is not None:
        line3 += progress_bar_styled(used_pct, 'ctx')
    else:
        line3 += fg(C['fText']) + ' ctx -- ' + R
    line3 += fg(C['bModel']) + DR + R

    line3 += SEP

    line3 += fg(C['bModel']) + DL + R
    if sess_used is not None:
        line3 += progress_bar_styled(sess_used, 'sess')
    else:
        line3 += fg(C['fText']) + ' sess -- ' + R
    line3 += fg(C['bModel']) + DR + R

    if reset_str:
        line3 += SEP + fg(C['fText']) + '⧖ ' + reset_str + R

    sys.stdout.write(line3 + '\n')
    sys.stdout.flush()


if __name__ == '__main__':
    main()
