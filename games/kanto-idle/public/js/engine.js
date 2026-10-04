// Motor del juego: estado, fórmulas y reglas. No toca el DOM, así se puede simular en Node.
import * as D from './data.js';

export const CFG = {
  killsToClear: 25,
  hpBase: 14,
  hpGrowth: 3.1,       // la vida de los salvajes se multiplica por esto en cada zona
  rewardBase: 3, rewardGrowth: 2.3, // ₽ por victoria = base × crecimiento^zona (crece más despacio que la vida)
  spawnDelay: 0.4,     // segundos entre un Pokémon derrotado y el siguiente (tope ≈ 2,5 victorias/s)
  gymHpK: 3,
  gymBase: 20, gymPerFight: 6,
  gymRewardK: 15,
  shinyOdds: 1 / 1024,
  legendTries: 3,
  // Pokémon
  powerDiv: 100, powerLvlDiv: 8, powerLvlExp: 1.6,
  teamDirect: 0.35,    // daño por segundo que aporta cada punto de poder del equipo
  teamMultK: 0.5,      // y cuánto multiplica a entrenadores y toques
  xpBase: 1, xpAreaScale: 0.3,
  xp0: 30, xp1: 2, xpExp: 2,
  // Toque
  glove: [1, 1.2, 0.05],
  techPct: 0.01,
  // Prestigio
  candyK: 1e5, candyExp: 0.5,
  candyDmg: 0.03,      // +3% de daño global por Caramelo Raro conseguido (acumulado)
  dexBonus: 0.02, shinyBonus: 0.03,
  offlineMax: 8 * 3600,
  autoTtk: 4,
  stoneKills: 25,      // una Piedra Evolutiva cuesta lo que ganas con ~25 victorias en tu zona más alta
};

let rng = Math.random;
export const setRng = (fn) => { rng = fn; };

// ---------- utilidades ----------
const SUFFIX = ['', 'K', 'M', 'B', 'T', 'Qa', 'Qi', 'Sx', 'Sp', 'Oc', 'No', 'Dc'];
export function fmt(n) {
  if (!isFinite(n)) return '∞';
  if (n < 0) return '-' + fmt(-n);
  const dec = (v, d) => v.toFixed(d).replace(/\.?0+$/, '').replace('.', ',');
  if (n < 1000) return n < 10 ? dec(n, 2) : n < 100 ? dec(n, 1) : String(Math.floor(n));
  const e = Math.floor(Math.log10(n) / 3);
  if (e >= SUFFIX.length) return n.toExponential(2).replace('e+', 'e').replace('.', ',');
  const v = n / Math.pow(1000, e);
  return dec(v, v < 10 ? 2 : v < 100 ? 1 : 0) + SUFFIX[e];
}
export function fmtTime(sec) {
  sec = Math.max(0, Math.floor(sec));
  const h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60), s = sec % 60;
  return h ? `${h} h ${m} min` : m ? `${m} min ${s} s` : `${s} s`;
}

export const areaHp = (i) => Math.round(CFG.hpBase * Math.pow(CFG.hpGrowth, i));
export const areaReward = (i) => Math.max(1, Math.round(CFG.rewardBase * Math.pow(CFG.rewardGrowth, i)));
export const xpNeed = (lvl) => Math.round(CFG.xp0 + CFG.xp1 * Math.pow(lvl, CFG.xpExp));
export const gymTime = (g) => g.time || CFG.gymBase + CFG.gymPerFight * g.fights.length;
export const gymFightHp = (g, fight) => areaHp(g.after) * fight.hp * (g === D.LEAGUE ? 1 : CFG.gymHpK);

// ---------- estado ----------
export function newState() {
  return {
    v: 1,
    starter: null,
    money: 0, runMoney: 0,
    area: 0, mode: 'wild', gym: null,
    cleared: {}, kills: {}, badges: [], leagueBeaten: false,
    owned: {},            // id -> {lvl, xp, shiny, gone}
    dex: {},              // id -> 1 (registrado) | 2 (shiny registrado)
    team: [null, null, null, null, null, null],
    trainers: {}, clickLvl: {}, upg: {}, stones: 0, masterBalls: 0,
    ball: 'poke',
    candies: 0, lifeCandies: 0, prestiges: 0, perks: {},
    ach: {},
    stats: { kills: 0, clicks: 0, caught: 0, shinies: 0, gymsWon: 0, leagueWins: 0, evolved: 0, lifeMoney: 0, flees: 0, playTime: 0 },
    settings: { autoNext: true, autoGym: false, autoLeague: false, autoEvolve: true, sound: false, wake: false, buyMult: 1 },
    last: Date.now(),
    enemy: null, spawnWait: 0, _dirty: true, _d: null, _t: 0, _autoT: 0, _gymCool: 0,
  };
}

const listeners = [];
export const onEvent = (fn) => listeners.push(fn);
const emit = (type, data) => { for (const fn of listeners) fn(type, data || {}); };

// ---------- recuentos ----------
export const dexCount = (s) => Object.keys(s.dex).length;
export const shinyCount = (s) => { let n = 0; for (const k in s.dex) if (s.dex[k] === 2) n++; return n; };
export const legendCount = (s) => { let n = 0; for (const k in s.dex) if (D.POKEMON[k].legendary) n++; return n; };
export const trainerCount = (s) => { let n = 0; for (const k in s.trainers) n += s.trainers[k]; return n; };
export const badgeCount = (s) => Math.min(8, s.badges.length);
export const levelCap = (s) => D.LEVEL_CAP[badgeCount(s)];
export const teamSlots = (s) => Math.min(6, 2 + Math.floor(badgeCount(s) / 2));
const U = { dexCount, shinyCount, legendCount, trainerCount };

// ---------- zonas ----------
export const MAX_AREA = 99;
export const areaDef = (k) => D.AREAS[Math.min(k, D.AREAS.length - 1)];
export function areaName(k) {
  const last = D.AREAS.length - 1;
  return k <= last ? D.AREAS[k].name : `${D.AREAS[last].name} · piso ${k - last + 1}`;
}
export function areaUnlocked(s, k) {
  if (k < 0 || k > MAX_AREA) return false;
  if (k === 0) return true;
  if (k >= D.AREAS.length) return !!s.cleared[k - 1] && areaUnlocked(s, D.AREAS.length - 1);
  const prev = D.AREAS[k - 1];
  if (!s.cleared[k - 1]) return false;
  if (prev.gym !== undefined && !s.badges.includes(prev.gym)) return false;
  if (D.AREAS[k].needsLeague && !s.leagueBeaten) return false;
  return true;
}
export function maxArea(s) { let m = 0; for (let i = 0; i <= MAX_AREA; i++) { if (areaUnlocked(s, i)) m = i; else break; } return m; }

export function gymAvailable(s, idx) {
  if (idx === 'league') return s.badges.length >= 8 && !!s.cleared[D.LEAGUE.after];
  const g = D.GYMS[idx];
  return !!s.cleared[g.after];
}

// ---------- cálculo derivado ----------
const pokePower = (p, id) => (D.POKEMON[id].bst / CFG.powerDiv) * Math.pow(p.lvl / CFG.powerLvlDiv, CFG.powerLvlExp) * (p.shiny ? 1.5 : 1);
export const milestoneMult = (n) => { let m = 1; for (const t of D.MILESTONES) if (n >= t) m *= 2; return m; };
export const nextMilestone = (n) => D.MILESTONES.find((t) => n < t) || null;
export const baseClick = (lvl) => CFG.glove[0] + CFG.glove[1] * lvl + CFG.glove[2] * lvl * lvl;

export function stonePrice(s) {
  return Math.max(1, Math.round(CFG.stoneKills * areaReward(maxArea(s)) * (s.perks.p_stone ? 0.5 : 1)));
}
export function ballCost(s, ball) {
  const b = D.BALLS.find((x) => x.id === ball);
  return Math.round(b.price * areaReward(s.area) * 0.6);
}

function compute(s) {
  const m = { money: 1, xp: 1, team: 1, trainers: 1, click: 1, all: 1, catch: 1 };
  for (const u of D.UPGRADES) if (s.upg[u.id]) m[u.kind] *= u.value;
  if (s.perks.p_xp) m.xp *= 1.5;
  if (s.perks.p_money) m.money *= 1.5;
  const slots = teamSlots(s);
  let power = 0;
  for (let i = 0; i < slots; i++) {
    const id = s.team[i];
    if (id && s.owned[id] && !s.owned[id].gone) power += pokePower(s.owned[id], id);
  }
  const teamMult = 1 + power * CFG.teamMultK;
  let trainerDps = 0;
  for (const t of D.TRAINERS) {
    const n = s.trainers[t.id] || 0;
    if (n) trainerDps += n * t.dps * milestoneMult(n);
  }
  const global = (1 + CFG.dexBonus * dexCount(s) + CFG.shinyBonus * shinyCount(s))
    * (1 + CFG.candyDmg * s.lifeCandies)
    * (1 + D.ACHIEVEMENT_BONUS * Object.keys(s.ach).length)
    * m.all;
  const base = power * CFG.teamDirect * m.team + trainerDps * m.trainers;
  const dps = base * teamMult * global;
  const glove = s.clickLvl.glove || 0, tech = s.clickLvl.tech || 0;
  const click = baseClick(glove) * m.click * global * (1 + power * CFG.teamMultK * 0.25) + dps * CFG.techPct * tech;
  return {
    power, teamMult, trainerDps, global, dps, click, slots,
    trainerMult: m.trainers, clickMult: m.click,
    moneyMult: m.money, xpMult: m.xp, catchMult: m.catch,
    shinyOdds: CFG.shinyOdds * (s.perks.p_iris ? 2 : 1),
  };
}
export function derive(s) {
  if (!s._d || s._dirty) { s._d = compute(s); s._dirty = false; }
  return s._d;
}
export const dirty = (s) => { s._dirty = true; };

// ---------- apariciones ----------
function pickSpecies(s) {
  const area = areaDef(s.area);
  let total = 0;
  const list = [];
  for (const [id, w] of area.pool) {
    const p = D.POKEMON[id];
    if (p.legendary && s.owned[id]) continue;
    if (id === 151 && s.prestiges < 1) continue;
    list.push([id, w]); total += w;
  }
  let r = rng() * total;
  for (const [id, w] of list) { r -= w; if (r <= 0) return id; }
  return list[list.length - 1][0];
}

function spawn(s) {
  if (s.mode === 'gym') {
    const g = s.gym.def, f = g.fights[s.gym.fight];
    const hp = gymFightHp(g, f);
    s.enemy = { id: f.sprite, label: f.label, shiny: false, hp, max: hp, boss: true };
    return;
  }
  const id = pickSpecies(s);
  const hp = areaHp(s.area);
  s.enemy = { id, shiny: rng() < derive(s).shinyOdds, hp, max: hp, legend: D.POKEMON[id].legendary };
  if (s.enemy.shiny) emit('shinySeen', { id });
}

function respawn(s, wait = CFG.spawnDelay) { s.enemy = null; s.spawnWait = wait; }

export function goArea(s, k) {
  if (s.mode !== 'wild' || !areaUnlocked(s, k)) return false;
  s.area = k; respawn(s, 0); emit('area', { area: k }); return true;
}

// ---------- recompensas ----------
function addMoney(s, n) {
  s.money += n; s.runMoney += n; s.stats.lifeMoney += n;
}

function gainXp(s, id, amount) {
  const o = s.owned[id];
  if (!o) return;
  const cap = levelCap(s);
  if (o.lvl >= cap) return;
  o.xp += amount;
  let up = false;
  while (o.lvl < cap && o.xp >= xpNeed(o.lvl)) { o.xp -= xpNeed(o.lvl); o.lvl++; up = true; }
  if (o.lvl >= cap) o.xp = 0;
  if (up) {
    s._dirty = true;
    emit('level', { id, lvl: o.lvl });
    const evo = D.POKEMON[id].evo;
    if (s.settings.autoEvolve && evo && evo[1] > 0 && !Array.isArray(evo[0]) && o.lvl >= evo[1]) evolve(s, id, evo[0]);
  }
}
function xpForKill(s) { return CFG.xpBase * (1 + s.area * CFG.xpAreaScale) * derive(s).xpMult; }
function giveTeamXp(s, amount) {
  for (let i = 0; i < teamSlots(s); i++) { const id = s.team[i]; if (id && s.owned[id] && !s.owned[id].gone) gainXp(s, id, amount); }
}

function register(s, id, shiny) {
  const had = !!s.owned[id];
  if (!had) s.owned[id] = { lvl: 5, xp: 0, shiny: false, gone: false };
  if (shiny) s.owned[id].shiny = true;
  s.dex[id] = Math.max(s.dex[id] || 0, shiny ? 2 : 1);
  s._dirty = true;
  return !had;
}

function chooseBall(s, legend) {
  const order = ['master', 'ultra', 'great', 'poke'];
  const want = order.indexOf(s.ball);
  for (let i = want; i < order.length; i++) {
    const b = order[i];
    if (b === 'master') { if (legend && s.masterBalls > 0 && s.ball === 'master') return b; continue; }
    if (s.money >= ballCost(s, b)) return b;
  }
  return null;
}

function tryCatch(s, e) {
  const sp = D.POKEMON[e.id];
  const have = s.owned[e.id];
  if (have && (!e.shiny || have.shiny)) return;
  const tries = e.legend ? CFG.legendTries : 1;
  for (let t = 0; t < tries; t++) {
    const ball = chooseBall(s, e.legend);
    if (!ball) { emit('noBalls', {}); return; }
    if (ball === 'master') s.masterBalls--; else s.money -= ballCost(s, ball);
    const b = D.BALLS.find((x) => x.id === ball);
    let p = e.legend ? D.LEGENDARY_CATCH[ball] : Math.min(1, (sp.catchRate / 255) * b.mult * derive(s).catchMult);
    if (e.shiny && !e.legend) p = Math.max(p, 0.6);
    if (rng() < p) {
      const isNew = register(s, e.id, e.shiny);
      s.stats.caught++;
      if (e.shiny) s.stats.shinies++;
      emit('catch', { id: e.id, shiny: e.shiny, isNew, legend: e.legend });
      return;
    }
  }
  s.stats.flees++;
  emit('flee', { id: e.id, shiny: e.shiny });
}

function defeatWild(s) {
  const e = s.enemy;
  const d = derive(s);
  addMoney(s, areaReward(s.area) * d.moneyMult);
  s.stats.kills++;
  s.kills[s.area] = (s.kills[s.area] || 0) + 1;
  if (!s.cleared[s.area] && s.kills[s.area] >= CFG.killsToClear) { s.cleared[s.area] = true; emit('cleared', { area: s.area }); }
  giveTeamXp(s, xpForKill(s));
  tryCatch(s, e);
  respawn(s);
}

function defeatBoss(s) {
  const g = s.gym.def;
  s.gym.fight++;
  if (s.gym.fight >= g.fights.length) return winGym(s);
  emit('bossStep', { fight: s.gym.fight });
  respawn(s, 0.12);
}

function winGym(s) {
  const key = s.gym.key;
  const g = s.gym.def;
  const first = key === 'league' ? !s.leagueBeaten : !s.badges.includes(key);
  if (first) {
    addMoney(s, areaReward(g.after) * CFG.gymRewardK * derive(s).moneyMult);
    if (key === 'league') { s.leagueBeaten = true; } else s.badges.push(key);
    s.stats.gymsWon++;
  }
  if (key === 'league') s.stats.leagueWins++;
  s.mode = 'wild'; s.gym = null; s._dirty = true;
  emit('gymWin', { key, first });
  respawn(s, 0.3);
}

function failGym(s) {
  const key = s.gym.key;
  s.mode = 'wild'; s.gym = null; s._gymCool = 15;
  emit('gymFail', { key });
  respawn(s, 0.3);
}

export function startGym(s, key) {
  if (s.mode !== 'wild' || !gymAvailable(s, key)) return false;
  const def = key === 'league' ? D.LEAGUE : D.GYMS[key];
  s.mode = 'gym';
  s.gym = { key, def, fight: 0, time: gymTime(def) };
  respawn(s, 0);
  emit('gymStart', { key });
  return true;
}
export function leaveGym(s) {
  if (s.mode !== 'gym') return;
  s.mode = 'wild'; s.gym = null; respawn(s, 0.2);
}
export function gymEstimate(s, key) {
  const def = key === 'league' ? D.LEAGUE : D.GYMS[key];
  let hp = 0;
  for (const f of def.fights) hp += gymFightHp(def, f);
  const dps = derive(s).dps;
  const need = hp / Math.max(dps, 1e-9) + def.fights.length * 0.12;
  return { hp, time: gymTime(def), need, ok: need <= gymTime(def) * 0.92 };
}

// ---------- combate ----------
function defeat(s) {
  if (s.mode === 'gym') defeatBoss(s); else defeatWild(s);
}

export function click(s) {
  s.stats.clicks++;
  if (!s.enemy) return 0;
  const dmg = derive(s).click;
  s.enemy.hp -= dmg;
  if (s.enemy.hp <= 0) defeat(s);
  return dmg;
}

export function tick(s, dt) {
  s.stats.playTime += dt;
  if (s.mode === 'gym') {
    s.gym.time -= dt;
    if (s.gym.time <= 0) { failGym(s); return; }
  }
  let t = dt, guard = 0;
  while (t > 0 && guard++ < 40) {
    if (!s.enemy) {
      if (s.spawnWait > t) { s.spawnWait -= t; break; }
      t -= s.spawnWait; s.spawnWait = 0; spawn(s); continue;
    }
    const dps = derive(s).dps; // se recalcula: subir de nivel a mitad de tick cambia el daño
    if (dps <= 0) break;
    const need = s.enemy.hp / dps;
    if (need > t) { s.enemy.hp -= dps * t; break; }
    t -= need; s.enemy.hp = 0; defeat(s);
  }
  s._t += dt; s._autoT += dt; s._gymCool = Math.max(0, s._gymCool - dt);
  if (s._autoT >= 0.5) { s._autoT = 0; autoActions(s); }
  if (s._t >= 1) { s._t = 0; checkAchievements(s); }
}

export const autoGymUnlocked = (s) => !!s.perks.p_auto || s.stats.gymsWon >= 1;

function autoActions(s) {
  if (s.mode !== 'wild') return;
  if (s._gymCool <= 0 && s.settings.autoGym && autoGymUnlocked(s)) {
    for (let i = 0; i < D.GYMS.length; i++) {
      if (!s.badges.includes(i) && gymAvailable(s, i)) { if (gymEstimate(s, i).ok) startGym(s, i); return; }
    }
    if (s.settings.autoLeague && !s.leagueBeaten && gymAvailable(s, 'league') && gymEstimate(s, 'league').ok) { startGym(s, 'league'); return; }
  }
  if (s.settings.autoNext && s.cleared[s.area] && areaUnlocked(s, s.area + 1)) {
    const ttk = areaHp(s.area + 1) / Math.max(derive(s).dps, 1e-9);
    if (ttk <= CFG.autoTtk) goArea(s, s.area + 1);
  }
}

export function checkAchievements(s) {
  for (const a of D.ACHIEVEMENTS) {
    if (!s.ach[a.id] && a.test(s, U)) { s.ach[a.id] = Date.now(); s._dirty = true; emit('ach', { id: a.id }); }
  }
}

// ---------- evolución ----------
export function canEvolve(s, id) {
  const o = s.owned[id], evo = D.POKEMON[id].evo;
  if (!o || o.gone || !evo) return false;
  return evo[1] === 0 ? s.stones > 0 : o.lvl >= evo[1];
}
export function evolve(s, id, to) {
  if (!canEvolve(s, id)) return false;
  const o = s.owned[id], evo = D.POKEMON[id].evo;
  const target = Array.isArray(evo[0]) ? to : evo[0];
  if (!target || (Array.isArray(evo[0]) && !evo[0].includes(target))) return false;
  if (evo[1] === 0) s.stones--;
  o.gone = true;
  const had = s.owned[target];
  if (had) { had.gone = false; had.lvl = Math.max(had.lvl, o.lvl); had.shiny = had.shiny || o.shiny; }
  else s.owned[target] = { lvl: o.lvl, xp: o.xp, shiny: o.shiny, gone: false };
  s.dex[target] = Math.max(s.dex[target] || 0, o.shiny ? 2 : 1);
  if (o.shiny) s.dex[target] = 2;
  const inTeam = s.team.includes(target);
  for (let i = 0; i < s.team.length; i++) if (s.team[i] === id) s.team[i] = inTeam ? null : target;
  s.stats.evolved++; s._dirty = true;
  emit('evolve', { from: id, to: target });
  return true;
}

// ---------- equipo ----------
export function chooseStarter(s, id) {
  register(s, id, false);
  s.team[0] = id; s.starter = id;
  s.stats.caught++;
  respawn(s, 0); s._dirty = true;
}
export function setTeamSlot(s, slot, id) {
  if (slot < 0 || slot >= 6) return false;
  if (id !== null) {
    const o = s.owned[id];
    if (!o || o.gone) return false;
    const at = s.team.indexOf(id);
    if (at >= 0) s.team[at] = s.team[slot];
  }
  s.team[slot] = id; s._dirty = true;
  return true;
}
export function bestTeam(s) {
  const list = Object.keys(s.owned).map(Number).filter((id) => !s.owned[id].gone)
    .sort((a, b) => pokePower(s.owned[b], b) - pokePower(s.owned[a], a));
  return list.slice(0, 6);
}
export function autoTeam(s) {
  const best = bestTeam(s);
  for (let i = 0; i < 6; i++) s.team[i] = best[i] || null;
  s._dirty = true;
}
export const pokeDps = (s, id) => { const o = s.owned[id]; return o ? pokePower(o, id) * CFG.teamDirect : 0; };
export const pokePowerOf = (s, id) => pokePower(s.owned[id], id);

// ---------- compras ----------
export function trainerCost(s, id, n = 1) {
  const t = D.TRAINERS.find((x) => x.id === id), k = s.trainers[id] || 0, g = D.TRAINER_GROWTH;
  return Math.ceil(t.cost * Math.pow(g, k) * (Math.pow(g, n) - 1) / (g - 1));
}
export function trainerMax(s, id) {
  const t = D.TRAINERS.find((x) => x.id === id), k = s.trainers[id] || 0, g = D.TRAINER_GROWTH;
  const first = t.cost * Math.pow(g, k);
  if (s.money < first) return 0;
  let n = Math.max(1, Math.floor(Math.log(s.money * (g - 1) / first + 1) / Math.log(g)));
  while (n > 1 && trainerCost(s, id, n) > s.money) n--;
  return trainerCost(s, id, n) <= s.money ? n : 0;
}
export function trainerUnlocked(s, i) {
  if (i === 0) return true;
  const prev = D.TRAINERS[i - 1];
  return (s.trainers[prev.id] || 0) > 0 || (s.trainers[D.TRAINERS[i].id] || 0) > 0 || s.runMoney >= D.TRAINERS[i].cost * 0.4;
}
export function buyTrainer(s, id, n) {
  if (n === 'max') n = trainerMax(s, id);
  if (n < 1) return false;
  const cost = trainerCost(s, id, n);
  if (s.money < cost) return false;
  s.money -= cost; s.trainers[id] = (s.trainers[id] || 0) + n; s._dirty = true;
  return true;
}
export function clickUpgCost(s, id) {
  const u = D.CLICK_UPGRADES.find((x) => x.id === id);
  return Math.ceil(u.cost * Math.pow(u.growth, s.clickLvl[id] || 0));
}
export function buyClickUpg(s, id) {
  const u = D.CLICK_UPGRADES.find((x) => x.id === id);
  if (u.max && (s.clickLvl[id] || 0) >= u.max) return false;
  const c = clickUpgCost(s, id);
  if (s.money < c) return false;
  s.money -= c; s.clickLvl[id] = (s.clickLvl[id] || 0) + 1; s._dirty = true;
  return true;
}
export const upgradeCost = (u) => Math.round(D.UPGRADE_COST_FACTOR * areaReward(u.area));
export function upgradeVisible(s, u) { return areaUnlocked(s, u.area); }
export function buyUpgrade(s, id) {
  const u = D.UPGRADES.find((x) => x.id === id);
  if (s.upg[id] || !upgradeVisible(s, u)) return false;
  const c = upgradeCost(u);
  if (s.money < c) return false;
  s.money -= c; s.upg[id] = true; s._dirty = true;
  return true;
}
export function buyStone(s) {
  const c = stonePrice(s);
  if (s.money < c) return false;
  s.money -= c; s.stones++; return true;
}
export function buyPerk(s, id) {
  const p = D.PERKS.find((x) => x.id === id);
  if (s.perks[id] || s.candies < p.cost) return false;
  s.candies -= p.cost; s.perks[id] = true; s._dirty = true;
  return true;
}
export function buyMasterBall(s) {
  if (s.candies < D.MASTER_BALL_CANDY_COST) return false;
  s.candies -= D.MASTER_BALL_CANDY_COST; s.masterBalls++;
  return true;
}

// ---------- prestigio ----------
export function candyGain(s) { return Math.floor(Math.pow(s.runMoney / CFG.candyK, CFG.candyExp)); }
export function prestige(s) {
  const gain = candyGain(s);
  if (gain < 1) return 0;
  s.candies += gain; s.lifeCandies += gain; s.prestiges++;
  s.money = s.perks.p_start ? 2000 : 0; s.runMoney = 0;
  s.area = 0; s.mode = 'wild'; s.gym = null;
  s.cleared = {}; s.kills = {}; s.badges = []; s.leagueBeaten = false;
  s.trainers = {}; s.clickLvl = {}; s.upg = {}; s.stones = 0;
  for (const id in s.owned) { s.owned[id].lvl = 5; s.owned[id].xp = 0; }
  s._dirty = true; respawn(s, 0);
  emit('prestige', { gain });
  return gain;
}

// ---------- sin conexión ----------
export function offline(s, seconds) {
  seconds = Math.min(seconds, CFG.offlineMax);
  if (seconds < 30 || !s.starter) return null;
  if (s.mode === 'gym') leaveGym(s);
  const eff = s.perks.p_away ? 0.8 : 0.5;
  const d = derive(s);
  const hp = areaHp(s.area);
  const perKill = hp / Math.max(d.dps, 1e-9) + CFG.spawnDelay;
  const kills = Math.floor(seconds * eff / perKill);
  if (kills < 1) return { seconds, kills: 0, money: 0 };
  const money = kills * areaReward(s.area) * d.moneyMult;
  addMoney(s, money);
  s.stats.kills += kills;
  s.kills[s.area] = (s.kills[s.area] || 0) + kills;
  if (!s.cleared[s.area] && s.kills[s.area] >= CFG.killsToClear) s.cleared[s.area] = true;
  giveTeamXp(s, xpForKill(s) * kills);
  s.stats.playTime += seconds;
  return { seconds, kills, money };
}

// ---------- guardado ----------
const KEY = 'kanto-idle-save';
export function serialize(s) {
  const { enemy, _d, _dirty, _t, _autoT, _gymCool, spawnWait, gym, ...rest } = s;
  rest.last = Date.now();
  rest.gymKey = gym ? gym.key : null;
  return JSON.stringify(rest);
}
export function hydrate(json) {
  const raw = JSON.parse(json);
  const s = newState();
  for (const k of Object.keys(raw)) {
    if (k === 'gymKey') continue;
    if (raw[k] && typeof raw[k] === 'object' && !Array.isArray(raw[k]) && s[k] && typeof s[k] === 'object') Object.assign(s[k], raw[k]);
    else s[k] = raw[k];
  }
  s.mode = 'wild'; s.gym = null; s.enemy = null; s._dirty = true;
  if (!areaUnlocked(s, s.area)) s.area = 0;
  return s;
}
export function save(s) { try { localStorage.setItem(KEY, serialize(s)); return true; } catch { return false; } }
export function load() { try { const j = localStorage.getItem(KEY); return j ? hydrate(j) : null; } catch { return null; } }
export function wipe() { try { localStorage.removeItem(KEY); } catch { /* sin almacenamiento */ } }
export function exportSave(s) {
  const bytes = new TextEncoder().encode(serialize(s));
  let bin = ''; for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin);
}
export function importSave(text) {
  const bin = atob(text.trim());
  const bytes = Uint8Array.from(bin, (c) => c.charCodeAt(0));
  const s = hydrate(new TextDecoder().decode(bytes));
  if (typeof s.v !== 'number') throw new Error('Guardado inválido');
  return s;
}
