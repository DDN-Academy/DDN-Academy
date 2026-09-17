const { chromium } = require('playwright-core');
const path = require('path');
(async () => {
  const D = __dirname;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const pg = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 3 });
  await pg.goto('file://' + path.join(D, 'one-page.html'), { waitUntil: 'networkidle' });
  await pg.evaluate(() => document.fonts.ready);
  const fit = await pg.evaluate(() => {
    const p = document.querySelector('.page'), pr = p.getBoundingClientRect();
    let max = 0;
    p.querySelectorAll(':scope > *').forEach(el => { const r = el.getBoundingClientRect(); if (r.bottom > max) max = r.bottom; });
    const px = 96/25.4;
    return { used: +((max - pr.top)/px).toFixed(1), limit: +((297 - 8)).toFixed(1) };
  });
  console.log('used ' + fit.used + 'mm / limit ' + fit.limit + 'mm  -> ' + (fit.used > fit.limit ? 'OVERFLOW ' + (fit.used-fit.limit).toFixed(1) : 'ok, ' + (fit.limit-fit.used).toFixed(1) + 'mm spare'));
  await pg.locator('.page').screenshot({ path: path.join(D, 'PANDA-One-Page.png') });
  await pg.pdf({ path: path.join(D, 'PANDA-One-Page.pdf'), width: '210mm', height: '297mm',
                 printBackground: true, margin: {top:'0',bottom:'0',left:'0',right:'0'} });
  await b.close();
})();
