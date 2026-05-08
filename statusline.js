const fs = require('fs');
const os = require('os');

let raw = '';
process.stdin.on('data', c => raw += c);
process.stdin.on('end', () => {
  let d = {};
  try { d = JSON.parse(raw); } catch(e) {}

  const R = '\x1b[0m';
  const B = '\x1b[1m';

  const fg = (hex) => {
    const r = parseInt(hex.slice(1,3),16), g = parseInt(hex.slice(3,5),16), b = parseInt(hex.slice(5,7),16);
    return `\x1b[38;2;${r};${g};${b}m`;
  };
  const bg = (hex) => {
    const r = parseInt(hex.slice(1,3),16), g = parseInt(hex.slice(3,5),16), b = parseInt(hex.slice(5,7),16);
    return `\x1b[48;2;${r};${g};${b}m`;
  };

  // if_tea.omp.json palette
  const C = {
    bSysinfo:  '#00c7fc',
    bExectime: '#2343e2',
    bShell:    '#91f2ff',
    bTime:     '#ff8c94',
    bPath:     '#f8677b',
    bModel:    '#1865f5',
    fDark:     '#000000',
    fWhite:    '#ffffff',
    fStatus:   '#00BCF9',
    fText:     '#91f2ff',
    pGreen:    '#00dc53',
    pYellow:   '#ffdc00',
    pRed:      '#ff0000',
  };

  // Nerd Font glyphs
  const DL = '';  // left rounded cap
  const DR = '';  // right rounded cap
  const SEP = '\x1b[2m' + fg(C.fText) + ' │ ' + R;

  // ── Data ─────────────────────────────────────────────────────────────
  const model = d.model || {};
  let modelName = (typeof model === 'object')
    ? (model.display_name || model.id || 'Claude')
    : String(model || 'Claude');
  modelName = modelName.replace(/^Claude /, '').replace(/^claude-/, '');

  const cwd  = d.cwd || '';
  const home = process.env.HOME || process.env.USERPROFILE || '';
  const displayDir = (home && cwd.startsWith(home))
    ? '~' + cwd.slice(home.length).replace(/\\/g, '/')
    : (cwd || '~');

  const ctx     = d.context_window || {};
  const usedPct = ctx.used_percentage != null ? Math.round(ctx.used_percentage) : null;

  const costUsd = parseFloat((d.cost || {}).total_cost_usd || 0).toFixed(3);

  const sid = d.session_id || '';
  let elapsedStr = '0m 0s';
  if (sid) {
    const tsFile = '/tmp/claude_session_start_' + sid;
    let startTs;
    try { startTs = parseInt(fs.readFileSync(tsFile, 'utf8').trim()); } catch(e) {}
    if (!startTs || isNaN(startTs)) {
      startTs = Math.floor(Date.now() / 1000);
      try { fs.writeFileSync(tsFile, String(startTs)); } catch(e) {}
    }
    const elapsed = Math.max(0, Math.floor(Date.now() / 1000) - startTs);
    elapsedStr = Math.floor(elapsed / 60) + 'm ' + (elapsed % 60) + 's';
  }

  const rl     = d.rate_limits || {};
  const sessRl = rl.five_hour || rl.session || {};
  const sessUsed = sessRl.used_percentage != null ? Math.round(sessRl.used_percentage) : null;
  const sessLeft = sessUsed !== null ? 100 - sessUsed : null;

  let resetStr = null;
  if (sessRl.resets_at) {
    const ts = typeof sessRl.resets_at === 'number'
      ? sessRl.resets_at * 1000
      : new Date(sessRl.resets_at).getTime();
    const diffMs = ts - Date.now();
    if (diffMs > 0) {
      const s = Math.floor(diffMs / 1000);
      const h = Math.floor(s / 3600);
      const m = Math.floor((s % 3600) / 60);
      resetStr = h > 0 ? (h + 'h ' + m + 'm') : (m + 'm ' + (s % 60) + 's');
    } else {
      resetStr = 'now';
    }
  }

  // System info
  function getCpuPct() {
    const cpus = os.cpus();
    let idle = 0, total = 0;
    cpus.forEach(c => { for (const k in c.times) total += c.times[k]; idle += c.times.idle; });
    return Math.round((1 - idle / total) * 100);
  }
  const cpuPct   = getCpuPct();
  const totalMem = os.totalmem();
  const usedMem  = totalMem - os.freemem();
  const ramUsed  = (usedMem  / 1073741824).toFixed(1);
  const ramTotal = (totalMem / 1073741824).toFixed(1);

  const now     = new Date();
  const timeStr = now.toLocaleTimeString('en-US', { hour:'2-digit', minute:'2-digit', second:'2-digit', hour12:true });
  const dayStr  = now.toLocaleDateString('en-US', { weekday:'long' });
  const shell   = (process.env.SHELL || process.env.ComSpec || 'bash').split(/[/\\]/).pop().replace('.exe','');

  // Progress bar
  const BAR = 14;
  function progressBar(pct, invert) {
    const danger = invert ? pct < 20 : pct > 80;
    const warn   = invert ? pct < 50 : pct > 50;
    const color  = danger ? C.pRed : warn ? C.pYellow : C.pGreen;
    const filled = Math.min(Math.round(pct * BAR / 100), BAR);
    return fg(color) + '█'.repeat(filled) + R + '\x1b[2m' + fg(color) + '░'.repeat(BAR - filled) + R;
  }

  // ── LINE 1: Model → CPU│RAM → ⏱elapsed → shell → 📁 dir ─────────────
  let line1 = '';
  line1 += fg(C.bModel) + DL + R + bg(C.bModel) + fg(C.fWhite) + B + ' ' + modelName + ' ' + R + fg(C.bModel) + bg(C.bSysinfo) + DR + R;
  line1 += bg(C.bSysinfo) + fg(C.fDark) + B + ' CPU: ' + cpuPct + '% │ RAM: ' + ramUsed + '/' + ramTotal + 'GB ' + R;
  line1 += fg(C.bSysinfo) + bg(C.bExectime) + DR + R;
  line1 += bg(C.bExectime) + fg(C.fWhite) + B + ' ⧖ ' + elapsedStr + ' ' + R;
  line1 += fg(C.bExectime) + bg(C.bShell) + DR + R;
  line1 += bg(C.bShell) + fg(C.fDark) + B + ' ' + shell + ' ' + R;
  line1 += fg(C.bShell) + bg(C.bPath) + DR + R;
  line1 += bg(C.bPath) + fg(C.fDark) + B + ' 📁 ' + displayDir + ' ' + R;
  line1 += fg(C.bPath) + DR + R;
  process.stdout.write(line1 + '\n');

  // ── LINE 2: $cost │ © time │ day 📅 ─────────────────────────────────
  let line2 = ' ';
  line2 += fg(C.bTime) + DL + R;
  line2 += bg(C.bTime) + fg(C.fDark) + B + ' $' + costUsd + ' │ © ' + timeStr + ' │ ' + dayStr + ' 📅 ' + R;
  line2 += fg(C.bTime) + DR + R;
  process.stdout.write(line2 + '\n');

  // ── LINE 3: [ctx bar] │ [sess bar] │ ⧖ reset ────────────────────────
  let line3 = ' ';

  function barColor(pct, invert) {
    const danger = invert ? pct < 20 : pct > 80;
    const warn   = invert ? pct < 50 : pct > 50;
    return danger ? C.pRed : warn ? C.pYellow : C.pGreen;
  }

  // EXTRA = proporcionalni dio (label i pct su fiksni, extra se dijeli po postotku)
  function progressBarStyled(pct, label) {
    const EXTRA     = 24;
    const extraBlue = Math.round(pct * EXTRA / 100);
    const extraCyan = EXTRA - extraBlue;
    return bg(C.bModel)   + fg(C.fDark) + ' ' + label + ' ' + ' '.repeat(extraBlue) + R
         + bg(C.bSysinfo) + fg(C.fDark) + ' '.repeat(extraCyan) + ' ' + pct + '% used ' + R;
  }

  // ctx: [DL label+bar pct DR] — DL/DR tamno plavi
  line3 += fg(C.bModel) + DL + R;
  line3 += usedPct !== null ? progressBarStyled(usedPct, 'ctx') : fg(C.fText) + ' ctx -- ' + R;
  line3 += fg(C.bModel) + DR + R;

  line3 += SEP;

  // sess: [DL label+bar pct DR] — DL/DR tamno plavi
  line3 += fg(C.bModel) + DL + R;
  line3 += sessUsed !== null ? progressBarStyled(sessUsed, 'sess') : fg(C.fText) + ' sess -- ' + R;
  line3 += fg(C.bModel) + DR + R;

  if (resetStr) line3 += SEP + fg(C.fText) + '⧖ ' + resetStr + R;

  process.stdout.write(line3 + '\n');
});
