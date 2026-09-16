const { chromium } = require('playwright-core');
const path = require('path');
(async () => {
  const D = __dirname;
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage();
  await page.goto('file://' + path.join(D, 'index.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);

  const report = await page.evaluate(() => {
    const MM = 297 * (96/25.4);           // page height in px
    const BOTTOM_PAD = 17 * (96/25.4);    // bottom padding
    const out = [];
    document.querySelectorAll('.page').forEach((p, i) => {
      const pr = p.getBoundingClientRect();
      let maxBottom = 0, tag = '';
      p.querySelectorAll('.body > *, .cover-in > *').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.bottom > maxBottom) { maxBottom = r.bottom; tag = el.className || el.tagName; }
      });
      const used = maxBottom - pr.top;
      const limit = MM - BOTTOM_PAD;
      out.push({ n: i+1, sec: p.getAttribute('data-sec') || 'cover',
                 usedMM: +( used / (96/25.4) ).toFixed(1),
                 limitMM: +( limit / (96/25.4) ).toFixed(1),
                 over: +(( used - limit ) / (96/25.4)).toFixed(1) });
    });
    return out;
  });
  console.log('PAGE  SECTION              USED    LIMIT   OVER');
  report.forEach(r => {
    const flag = r.over > 0 ? '  <<< OVERFLOW' : (r.over > -12 ? '  (tight)' : '');
    console.log(String(r.n).padEnd(6) + r.sec.padEnd(21) + String(r.usedMM).padStart(6) + String(r.limitMM).padStart(9) + String(r.over).padStart(8) + flag);
  });

  await page.pdf({ path: path.join(D, "PANDAs-Program.pdf"), width: '210mm', height: '297mm',
                   printBackground: true, margin: {top:'0',bottom:'0',left:'0',right:'0'}, preferCSSPageSize: false });
  await browser.close();
})();
