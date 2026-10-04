// Simulador de equilibrio: un "jugador" automático recorre el juego y mide cuánto tarda cada hito.
// Uso: node tools/sim.mjs [tapsPorSegundo=2] [horasMax=12] [prestigios=1]
import * as E from '../public/js/engine.js';
import * as D from '../public/js/data.js';

const taps = Number(process.argv[2] ?? 2);
const maxH = Number(process.argv[3] ?? 12);
const runs = Number(process.argv[4] ?? 1);
if (process.argv[5]) Object.assign(E.CFG, JSON.parse(process.argv[5]));
const QUIET = !!process.env.QUIET;
if (process.env.TR) { const [c, d] = process.env.TR.split(',').map(Number); D.TRAINERS.forEach((t, i) => { t.cost = 25 * Math.pow(c, i); t.dps = 0.6 * Math.pow(d, i); }); }

function mulberry(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
E.setRng(mulberry(42));

const s = E.newState();
s.settings.autoEvolve = true; s.settings.autoNext = true; s.settings.autoGym = true; s.settings.autoLeague = true;
E.chooseStarter(s, 4);
const milestones = [];
let T = 0;
const mark = (label) => milestones.push(`${(T / 60).toFixed(1).padStart(7)} min  ${label}`);
E.onEvent((type, d) => {
  if (type === 'gymWin' && d.first) mark(d.key === 'league' ? 'LIGA VENCIDA' : `medalla ${D.GYMS[d.key].leader}`);
  if (type === 'gymFail') mark(`  (derrota ${d.key === 'league' ? 'Liga' : D.GYMS[d.key].leader})`);
  if (type === 'area') mark(`zona ${d.area}: ${E.areaName(d.area)}  (dps ${E.fmt(E.derive(s).dps)})`);
  if (type === 'catch' && d.legend) mark(`legendario capturado: ${D.POKEMON[d.id].name}`);
});

// Valor de una compra = cuánto sube (dps + 2*toque) por ₽
function gain(fn) {
  const before = E.derive(s); const b = before.dps + before.click * taps;
  const snap = JSON.stringify({ t: s.trainers, c: s.clickLvl, u: s.upg, st: s.stones });
  fn(s); s._dirty = true;
  const after = E.derive(s); const a = after.dps + after.click * taps;
  const o = JSON.parse(snap); s.trainers = o.t; s.clickLvl = o.c; s.upg = o.u; s.stones = o.st; s._dirty = true;
  return a - b;
}
function bestPurchase() {
  const c = [];
  D.TRAINERS.forEach((t, i) => { if (E.trainerUnlocked(s, i)) { const cost = E.trainerCost(s, t.id, 1); c.push({ cost, g: gain((x) => { x.trainers[t.id] = (x.trainers[t.id] || 0) + 1; }), buy: () => E.buyTrainer(s, t.id, 1) }); } });
  for (const u of D.CLICK_UPGRADES) { if (u.max && (s.clickLvl[u.id] || 0) >= u.max) continue; const cost = E.clickUpgCost(s, u.id); c.push({ cost, g: gain((x) => { x.clickLvl[u.id] = (x.clickLvl[u.id] || 0) + 1; }), buy: () => E.buyClickUpg(s, u.id) }); }
  for (const u of D.UPGRADES) if (!s.upg[u.id] && E.upgradeVisible(s, u)) c.push({ cost: E.upgradeCost(u), g: gain((x) => { x.upg[u.id] = true; }), buy: () => E.buyUpgrade(s, u.id) });
  let best = null;
  for (const x of c) { if (x.g <= 0) continue; const r = x.cost / x.g; if (!best || r < best.r) best = { ...x, r }; }
  return best;
}

let step = 1;
let lastBuyCheck = 0;
function stoneAndTeam() {
  for (const id of Object.keys(s.owned).map(Number)) {
    const o = s.owned[id], evo = D.POKEMON[id].evo;
    if (evo && evo[1] === 0 && !o.gone && E.stonePrice(s) <= s.money * 0.3) { if (E.buyStone(s)) E.evolve(s, id, Array.isArray(evo[0]) ? evo[0][0] : evo[0]); }
  }
  E.autoTeam(s);
}

for (let r = 1; r <= runs; r++) {
  const startT = T;
  milestones.length = 0;
  mark(`--- inicio aventura ${r} ---`);
  let done = false;
  while (T - startT < maxH * 3600 && !done) {
    E.tick(s, step); T += step;
    for (let i = 0; i < taps; i++) E.click(s);
    if (s.mode === 'wild' && s._gymCool <= 0) {
      for (let i = 0; i < D.GYMS.length; i++) if (!s.badges.includes(i) && E.gymAvailable(s, i)) { if (E.gymEstimate(s, i).ok) E.startGym(s, i); break; }
      if (s.mode === 'wild' && !s.leagueBeaten && E.gymAvailable(s, 'league') && E.gymEstimate(s, 'league').ok) E.startGym(s, 'league');
    }
    if (T - lastBuyCheck >= 1) {
      lastBuyCheck = T;
      for (let k = 0; k < 60; k++) { const b = bestPurchase(); if (b && b.cost <= s.money) { b.buy(); } else break; }
      if (Math.floor(T) % 20 === 0) stoneAndTeam();
    }
    if (s.cleared[Number(process.env.DEPTH ?? 13)]) done = true;
  }
  const d = E.derive(s);
  console.log(`\n=== Aventura ${r}: ${(T - startT) / 60 | 0} min, zona ${s.area}, dps ${E.fmt(d.dps)}, click ${E.fmt(d.click)}, ₽ run ${E.fmt(s.runMoney)}, kills ${s.stats.kills}, dex ${E.dexCount(s)}, shinies ${E.shinyCount(s)}, candies si prestigio: ${E.candyGain(s)} ===`);
  if (process.env.DIAG) {
    console.log('trainers', JSON.stringify(s.trainers), 'clickLvl', JSON.stringify(s.clickLvl));
    console.log('upg', Object.keys(s.upg).length, 'power', E.fmt(d.power), 'teamMult', E.fmt(d.teamMult), 'global', d.global.toFixed(2), 'trainerDps(raw)', E.fmt(d.trainerDps), 'moneyMult', d.moneyMult);
    console.log('team lvls', s.team.map((id) => id && `${D.POKEMON[id].name} L${s.owned[id].lvl}`).join(', '), 'cap', E.levelCap(s));
  }
  console.log(QUIET ? milestones.filter((m) => /medalla|LIGA|derrota/.test(m)).join('\n') : milestones.join('\n'));
  if (r < runs) {
    const g = E.prestige(s); if (!g) { console.log('no se puede prestigiar'); break; }
    for (const id of ['p_money', 'p_xp', 'p_start', 'p_auto', 'p_stone', 'p_iris', 'p_away']) E.buyPerk(s, id);
    console.log(`  -> reinicio: +${g} caramelos (total ${s.lifeCandies}), perks: ${Object.keys(s.perks).join(',') || '-'}`);
    E.autoTeam(s);
  }
}
