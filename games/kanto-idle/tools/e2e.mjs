// Prueba de humo en navegador (móvil): arranca, elige inicial, toca, compra, recorre pestañas y captura pantallas.
// Uso: PLAYWRIGHT_MODULE=/ruta/a/playwright node tools/e2e.mjs [url] [carpetaCapturas]
import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';
const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || 'playwright');
const url = process.argv[2] || 'http://localhost:8099/index.html';
const out = process.argv[3] || '.tmp/shots';
mkdirSync(out, { recursive: true });

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 390, height: 780 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
const page = await ctx.newPage();
const errors = [];
page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
page.on('requestfailed', (r) => errors.push('requestfailed: ' + r.url()));

await page.goto(url);
await page.waitForSelector('.starters button');
await page.screenshot({ path: `${out}/01-starter.png` });
await page.click('.starters button:nth-child(2)');
await page.waitForTimeout(400);

const arena = page.locator('#arena');
for (let i = 0; i < 40; i++) { await arena.tap({ position: { x: 190 + (i % 5) * 8, y: 150 } }); }
await page.waitForTimeout(300);
await page.screenshot({ path: `${out}/02-battle.png` });
const money1 = await page.textContent('#money');

// Dar dinero y comprar para recorrer la tienda
await page.evaluate(async () => { const E = await import('./js/engine.js'); const UI = await import('./js/ui.js'); const s = UI.state(); s.money += 5000; s.runMoney += 5000; });
await page.click('#tabs [data-tab=shop]');
await page.waitForTimeout(500);
await page.locator('#trainerList .buy').first().click();
await page.locator('#trainerList .buy').first().click();
await page.screenshot({ path: `${out}/03-shop.png` });
await page.click('#shopSeg [data-sub=upgrades]'); await page.waitForTimeout(400);
await page.screenshot({ path: `${out}/04-upgrades.png` });
await page.click('#shopSeg [data-sub=store]'); await page.waitForTimeout(400);
await page.click('#tabs [data-tab=team]'); await page.waitForTimeout(400);
await page.screenshot({ path: `${out}/05-team.png` });
await page.click('#teamSlots .slot[data-poke]'); await page.waitForTimeout(300);
await page.screenshot({ path: `${out}/06-poke.png` });
await page.click('#modal [data-a=close]');
await page.click('#tabs [data-tab=dex]'); await page.waitForTimeout(400);
await page.screenshot({ path: `${out}/07-dex.png` });
await page.click('#tabs [data-tab=more]'); await page.waitForTimeout(400);
await page.screenshot({ path: `${out}/08-more.png` });
for (const sub of ['ach', 'reset', 'set']) { await page.click(`#moreSeg [data-sub=${sub}]`); await page.waitForTimeout(250); await page.screenshot({ path: `${out}/09-more-${sub}.png` }); }

// Que el motor avance solo y que se guarde
await page.click('#tabs [data-tab=battle]');
await page.waitForTimeout(3000);
const saved = await page.evaluate(() => localStorage.getItem('kanto-idle-save') ? 'ok' : 'no');
const sw = await page.evaluate(async () => { const r = await navigator.serviceWorker?.getRegistration(); return r ? 'registrado' : 'sin SW'; });
console.log(JSON.stringify({ money1, saved, sw, errors }, null, 1));
await browser.close();
