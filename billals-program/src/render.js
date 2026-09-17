const { chromium } = require('playwright-core');
const path = require('path');
(async () => {
  const D = __dirname;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const pg = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await pg.goto('file://' + path.join(D, 'index.html'), { waitUntil: 'networkidle' });
  await pg.evaluate(() => document.fonts.ready);
  const rep = await pg.evaluate(() => {
    const px = 96/25.4, LIMIT = 297 - 11;   // bottom padding 12mm, page-number sits at 6mm
    const out = [];
    document.querySelectorAll('.page').forEach((p,i) => {
      const pr = p.getBoundingClientRect(); let max = 0;
      p.querySelectorAll(':scope > *:not(.pnum)').forEach(el => { const r = el.getBoundingClientRect(); if (r.bottom > max) max = r.bottom; });
      out.push({ n:i+1, used:+((max-pr.top)/px).toFixed(1), limit:LIMIT });
    });
    return out;
  });
  rep.forEach(r => console.log('p' + r.n + '  used ' + r.used + 'mm / ' + r.limit + 'mm  ' +
    (r.used > r.limit ? '<<< OVERFLOW ' + (r.used-r.limit).toFixed(1) : 'ok (' + (r.limit-r.used).toFixed(1) + 'mm spare)')));
  await pg.pdf({ path: path.join(D, "BILLALs-Program.pdf"), width:'210mm', height:'297mm',
                 printBackground:true, margin:{top:'0',bottom:'0',left:'0',right:'0'} });
  await b.close();
})();
