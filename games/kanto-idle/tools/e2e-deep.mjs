// Prueba profunda: gimnasio, shiny, legendario, evolución, reinicio, offline, exportar/importar y modo sin conexión.
import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';
const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || 'playwright');
const url = process.argv[2] || 'http://localhost:8099/index.html';
const out = process.argv[3] || '.tmp/shots2';
mkdirSync(out, { recursive: true });
const results = [];
const check = (name, ok, extra = '') => { results.push(`${ok ? 'OK  ' : 'FALLA'} ${name} ${extra}`); };

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 390, height: 780 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
const page = await ctx.newPage();
const errors = [];
page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });

await page.goto(url);
await page.waitForSelector('.starters button');
await page.click('.starters button:nth-child(2)');
await page.waitForTimeout(300);
const run = (fn, arg) => page.evaluate(fn, arg);
const sim = (secs) => run(async (n) => { const E = await import('./js/engine.js'); const UI = await import('./js/ui.js'); const s = UI.state(); for (let i = 0; i < n * 10; i++) E.tick(s, 0.1); }, secs);

// --- preparar: zonas despejadas y dinero ---
await run(async () => {
  const E = await import('./js/engine.js'); const UI = await import('./js/ui.js'); const s = UI.state();
  s.cleared[0] = s.cleared[1] = s.cleared[2] = true; s.money = 1e6; s.runMoney = 1e6;
  s.trainers.t0 = 40; s.trainers.t1 = 6; s._dirty = true; E.goArea(s, 2);
});
await page.waitForTimeout(400);
await page.screenshot({ path: `${out}/01-gym-cta.png` });
const cta = await page.textContent('#gymCta');
check('CTA de gimnasio visible', /Brock/.test(cta), cta.slice(0, 60));

await page.click('#gymCta [data-a=gym]');
await page.waitForTimeout(500);
await page.screenshot({ path: `${out}/02-gym-fight.png` });
check('modo gimnasio activo', await page.isVisible('#gymTimer'));
await sim(40);
await page.waitForTimeout(500);
const badges = await run(async () => (await import('./js/ui.js')).state().badges.length);
check('medalla Roca ganada', badges === 1, `badges=${badges}`);
await page.screenshot({ path: `${out}/03-gym-won.png` });

// --- shiny + legendario + captura ---
await run(async () => {
  const UI = await import('./js/ui.js'); const s = UI.state();
  s.enemy = { id: 6, shiny: true, hp: 1e9, max: 1e9, legend: false };
});
await page.waitForTimeout(250);
await page.screenshot({ path: `${out}/04-shiny.png` });
check('chispas shiny', await page.evaluate(() => document.getElementById('enemyWrap').classList.contains('shiny')));
await run(async () => { const UI = await import('./js/ui.js'); const s = UI.state(); s.enemy = { id: 150, shiny: false, hp: 1e9, max: 1e9, legend: true }; });
await page.waitForTimeout(250);
check('etiqueta legendario', await page.isVisible('#legendTag'));
await page.screenshot({ path: `${out}/05-legend.png` });

// --- evolución ---
await run(async () => {
  const E = await import('./js/engine.js'); const UI = await import('./js/ui.js'); const s = UI.state();
  s.owned[4].lvl = 15; s.badges = [0]; s.settings.autoEvolve = false; s._dirty = true;
  s.owned[25] = { lvl: 8, xp: 0, shiny: false, gone: false }; s.dex[25] = 1; s.stones = 1; s.owned[133] = { lvl: 8, xp: 0, shiny: false, gone: false }; s.dex[133] = 1;
});
await page.click('#tabs [data-tab=team]'); await page.waitForTimeout(500);
check('punto rojo de evolución', await page.evaluate(() => document.querySelector('#tabs [data-tab=team]').classList.contains('dot')));
await run(async () => { const E = await import('./js/engine.js'); const UI = await import('./js/ui.js'); const s = UI.state(); s.owned[4].lvl = 16; s._dirty = true; });
await page.waitForTimeout(600);
await page.click('#teamSlots .slot[data-poke="4"]'); await page.waitForTimeout(300);
await page.screenshot({ path: `${out}/06-evolve-modal.png` });
await page.click('#modal [data-evo]'); await page.waitForTimeout(400);
const evolved = await run(async () => { const s = (await import('./js/ui.js')).state(); return s.team[0]; });
check('Charmander evoluciona a Charmeleon', evolved === 5, `team[0]=${evolved}`);
// Eevee: tres opciones
await page.click('#box .bx[data-poke="133"]'); await page.waitForTimeout(300);
const evoBtns = await page.locator('#modal [data-evo]').count();
check('Eevee ofrece 3 evoluciones', evoBtns === 3, `botones=${evoBtns}`);
await page.screenshot({ path: `${out}/07-eevee.png` });
await page.click('#modal [data-a=close]');

// --- pokédex ficha ---
await page.click('#tabs [data-tab=dex]'); await page.waitForTimeout(300);
await page.click('#dexGrid .dc[data-dex="25"]'); await page.waitForTimeout(300);
await page.screenshot({ path: `${out}/08-dex-detail.png` });
await page.click('#modal [data-a=close]');

// --- pestaña Más ---
await page.click('#tabs [data-tab=more]'); await page.waitForTimeout(300);
await page.screenshot({ path: `${out}/09-gyms.png` });

// --- reinicio ---
await run(async () => { const s = (await import('./js/ui.js')).state(); s.runMoney = 4e7; });
await page.click('#moreSeg [data-sub=reset]'); await page.waitForTimeout(300);
await page.screenshot({ path: `${out}/10-reset.png` });
await page.click('#more-reset [data-a=prestige]'); await page.waitForTimeout(300);
await page.screenshot({ path: `${out}/11-reset-confirm.png` });
await page.click('#modal [data-a=ok]'); await page.waitForTimeout(500);
const pr = await run(async () => { const s = (await import('./js/ui.js')).state(); return { p: s.prestiges, c: s.candies, area: s.area, badges: s.badges.length, dex: Object.keys(s.dex).length }; });
check('reinicio concede caramelos y conserva Pokédex', pr.p === 1 && pr.c === 20 && pr.area === 0 && pr.badges === 0 && pr.dex >= 4, JSON.stringify(pr));
await page.screenshot({ path: `${out}/12-after-reset.png` });

// --- exportar / importar ---
const code = await run(async () => { const E = await import('./js/engine.js'); const s = (await import('./js/ui.js')).state(); return E.exportSave(s); });
const back = await run(async (c) => { const E = await import('./js/engine.js'); const s = E.importSave(c); return { starter: s.starter, c: s.candies, dex: Object.keys(s.dex).length }; }, code);
check('exportar/importar conserva datos', back.c === 20 && back.starter === 4, JSON.stringify(back));

// --- offline: guardar, retroceder el reloj 2 h y recargar ---
const old = await run(async () => { const E = await import('./js/engine.js'); const s = (await import('./js/ui.js')).state(); s.trainers.t0 = 30; s._dirty = true; const j = JSON.parse(E.serialize(s)); j.last = Date.now() - 2 * 3600 * 1000; return JSON.stringify(j); });
await page.goto('about:blank'); // al salir, el juego guarda con la hora actual; el guardado antiguo se inyecta después
await page.addInitScript((j) => { if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1'); localStorage.setItem('kanto-idle-save', j); } }, old);
await page.goto(url);
await page.waitForSelector('#modal:not([hidden])', { timeout: 5000 }).catch(() => {});
const modalText = await page.textContent('#modalBox');
check('mensaje de bienvenida con progreso offline', /Bienvenido de nuevo/.test(modalText), modalText.slice(0, 120));
await page.screenshot({ path: `${out}/13-welcome-back.png` });

// --- sin conexión: el SW sirve el juego ---
await page.click('#modal [data-a=close]').catch(() => {});
await page.waitForTimeout(1500);
await ctx.setOffline(true);
await page.reload();
await page.waitForSelector('#arena', { timeout: 8000 }).then(() => check('arranca sin conexión', true)).catch(() => check('arranca sin conexión', false));
await page.waitForTimeout(1500);
const img = await page.evaluate(() => { const i = document.getElementById('enemyImg'); return i.complete && i.naturalWidth > 0; });
check('sprites desde caché sin conexión', img);
await ctx.setOffline(false);

console.log(results.join('\n'));
console.log('errores de consola:', JSON.stringify(errors));
await browser.close();
