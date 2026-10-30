// Run: npm i playwright@1.56.1 && node capture.js   (lab must be running on 127.0.0.1:3000)
// Captures report figures: live screenshots of the loopback lab, the saved ZAP report,
// terminal-style panels rendered from the real evidence .txt files, and an architecture diagram.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '../..');
const SHOTS = path.join(ROOT, 'evidence/06-screenshots');
const FIGS = path.join(ROOT, 'report/figures');
fs.mkdirSync(SHOTS, { recursive: true });
fs.mkdirSync(FIGS, { recursive: true });

const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const css = `
  body{margin:0;background:#0d1117;font-family:Segoe UI,Arial,sans-serif;color:#c9d1d9}
  .wrap{padding:22px;width:900px}
  h1{font-size:20px;margin:0 0 4px;color:#e6edf3} .sub{font-size:13px;color:#8b949e;margin-bottom:14px}
  pre{background:#010409;border:1px solid #30363d;border-radius:8px;padding:14px;margin:0;
      font:13px/1.45 Consolas,monospace;white-space:pre-wrap;word-break:break-all}
  .cmd{color:#7ee787} .hit{color:#ffa657;font-weight:bold} .good{color:#3fb950;font-weight:bold}
  .bad{color:#ff7b72;font-weight:bold} .foot{font-size:12px;color:#6e7681;margin-top:10px}`;

function panel(title, sub, file, opts = {}) {
  let lines = fs.readFileSync(path.join(ROOT, file), 'utf8').replace(/^\uFEFF/, '').split(/\r?\n/);
  if (opts.filter) lines = opts.filter(lines);
  const body = lines.map(l => {
    const e = esc(l);
    if (l.startsWith('>')) return `<span class="cmd">${e}</span>`;
    if (opts.bad && opts.bad.some(k => l.includes(k))) return `<span class="bad">${e}</span>`;
    if (opts.hit && opts.hit.some(k => l.includes(k))) return `<span class="hit">${e}</span>`;
    return e;
  }).join('\n');
  return `<html><head><style>${css}</style></head><body><div class="wrap">
    <h1>${title}</h1><div class="sub">${sub}</div><pre>${body.trim()}</pre>
    <div class="foot">Rendered from the team's evidence file <b>${file}</b> (unaltered text${opts.note ? '; ' + opts.note : ''}). Isolated local lab, synthetic data.</div>
  </div></body></html>`;
}

const panels = [
  ['fig-EV-001-nmap.png', panel('EV-001 — Nmap service discovery', 'Loopback only, single authorized port',
    'evidence/reconnaissance/EV-001-nmap-local-baseline.txt',
    { hit: ['3000/tcp open', 'ppp?'], note: 'service fingerprint block shortened',
      filter: ls => {
        const out = []; let n = 0;
        for (const l of ls) {
          if (!l.startsWith('SF')) { out.push(l); continue; }
          if (n < 3) out.push(l);
          if (++n === 3) out.push('   … (fingerprint continues — full text in EV-001)');
        }
        return out;
      } })],
  ['fig-ENV-002-isolation.png', panel('ENV-002 — Isolation check', 'Port bound to loopback; LAN address unreachable',
    'evidence/environment/isolation-check.txt', { hit: ['127.0.0.1:3000', 'Isolation confirmed', 'HTTP code: 000'] })],
  ['fig-WA-001-csp.png', panel('WA-001 — Missing Content-Security-Policy', 'Response headers of the home page',
    'evidence/manual-tests/WA-001-csp-headers.txt', { bad: ['NO - header absent'] })],
  ['fig-WA-002-cors.png', panel('WA-002 — Permissive CORS', 'Request sent with a foreign Origin header',
    'evidence/manual-tests/WA-002-cors-headers.txt', { bad: ['Access-Control-Allow-Origin: *'] })],
  ['fig-WA-004-idor.png', panel('WA-004 — IDOR on /rest/basket/:id', "User B's token retrieves user A's basket",
    'evidence/manual-tests/WA-004-idor-basket.txt', { bad: ['"UserId":25', 'HTTP/1.1 200 OK'], hit: ['basket id 6', 'basket id 7', '"bid":6', '"bid":7'], note: 'JWTs were already redacted in the file' })],
];

const arch = `<html><head><style>${css}
  .box{border:2px solid #30363d;border-radius:10px;padding:12px 16px;background:#161b22;text-align:center}
  .lab{border:2px dashed #3fb950;border-radius:14px;padding:18px;position:relative}
  .tag{position:absolute;top:-12px;left:16px;background:#0d1117;padding:0 8px;color:#3fb950;font-weight:bold;font-size:13px}
  .row{display:flex;gap:18px;justify-content:center;align-items:stretch}
  .arrow{color:#8b949e;text-align:center;font:13px Consolas,monospace;margin:8px 0}
  b{color:#e6edf3} .small{font-size:12px;color:#8b949e}
  .proxy{border-color:#d29922} .app{border-color:#58a6ff} .blocked{color:#ff7b72;text-align:center;margin-top:16px;font-size:13px}
</style></head><body><div class="wrap">
  <h1>Lab architecture</h1><div class="sub">Single Windows 11 laptop · everything bound to 127.0.0.1</div>
  <div class="lab"><span class="tag">ISOLATED LOCAL LAB (loopback only)</span>
    <div class="box"><b>Analyst tools</b><div class="small">Chrome 156 + DevTools · curl · PowerShell · Nmap 7.993 · OWASP ZAP 2.17.0 · Python 3.14 (team script)</div></div>
    <div class="row" style="margin-top:6px">
      <div style="flex:1"><div class="arrow">│ BEFORE<br>127.0.0.1:3000 (direct)<br>▼</div></div>
      <div style="flex:1"><div class="arrow">│ AFTER<br>127.0.0.1:8080<br>▼</div>
        <div class="box proxy"><b>csp-proxy</b> (Docker)<div class="small">nginx 1.27-alpine · adds Content-Security-Policy</div></div>
        <div class="arrow">▼ forwards to :3000</div></div>
    </div>
    <div class="box app"><b>juice-shop</b> (Docker) — OWASP Juice Shop 20.3.0<div class="small">Angular front end · Node.js REST API · JWT auth · in-container SQLite · synthetic data only</div></div>
  </div>
  <div class="blocked">✗ Host LAN address 192.168.199.1:3000 → connection fails (verified 2026-10-28)</div>
</div></body></html>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 944, height: 600 }, deviceScaleFactor: 1.5 });

  for (const [name, html] of [...panels, ['fig-architecture.png', arch]]) {
    await page.setContent(html);
    await page.locator('.wrap').screenshot({ path: path.join(FIGS, name) });
    console.log('figure', name);
  }

  // Live lab captures (loopback only)
  const live = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  await live.goto('http://127.0.0.1:3000/', { waitUntil: 'networkidle' });
  for (const sel of ['button:has-text("Dismiss")', 'a[aria-label="dismiss cookie message"]', 'text=Me want it!']) {
    try { await live.click(sel, { timeout: 3000 }); } catch {}
  }
  try { await live.waitForSelector('mat-card', { timeout: 15000 }); } catch { console.log('no product cards'); }
  await live.waitForTimeout(1500);
  await live.screenshot({ path: path.join(SHOTS, 'ENV-003-juice-shop-home.png') });
  console.log('live home');

  await live.goto('http://127.0.0.1:3000/ftp', { waitUntil: 'networkidle' });
  await live.screenshot({ path: path.join(SHOTS, 'WA-003-ftp-listing.png'), clip: { x: 0, y: 0, width: 1280, height: 260 } });
  console.log('live ftp');

  // Saved ZAP report: summary + alert list
  const zap = await browser.newPage({ viewport: { width: 1100, height: 800 } });
  await zap.goto('file:///' + path.join(ROOT, 'evidence/automated-scans/EV-002-zap-scan-raw.html').replace(/\\/g, '/'));
  const top = await zap.evaluate(() => {
    const h = [...document.querySelectorAll('h3')].find(e => e.textContent.trim().startsWith('Summary of Alerts'));
    return h ? h.getBoundingClientRect().top + window.scrollY - 10 : 0;
  });
  const bottom = await zap.evaluate(() => {
    const h = [...document.querySelectorAll('h3')].find(e => e.textContent.trim().startsWith('Alert Detail'));
    return h ? h.getBoundingClientRect().top + window.scrollY : 1200;
  });
  await zap.screenshot({ path: path.join(SHOTS, 'EV-002-zap-alert-summary.png'), fullPage: true,
    clip: { x: 0, y: top, width: 1100, height: Math.max(200, bottom - top) } });
  console.log('zap summary', top, bottom);

  await browser.close();
})();
