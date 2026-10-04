// Interfaz. El DOM se construye una vez y se actualiza en sitio: si se reconstruyera cada frame,
// un botón pulsado en el móvil podría desaparecer entre el toque y la suelta y el clic se perdería.
import * as E from './engine.js';
import * as D from './data.js';

const $ = (id) => document.getElementById(id);
const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
const sprite = (id, shiny) => `sprites/${shiny ? 'shiny' : 'pokemon'}/${id}.png`;
const pname = (id) => D.POKEMON[id].name;
const setText = (node, v) => { if (node._v !== v) { node._v = v; node.textContent = v; } };
const setHtml = (node, v) => { if (node._v !== v) { node._v = v; node.innerHTML = v; } };
const toggleCls = (node, c, on) => { if (node.classList.contains(c) !== on) node.classList.toggle(c, on); };

let S = null;
let hooks = {};
const ui = { tab: 'battle', shopSub: 'trainers', moreSub: 'gyms', teamDirty: true, enemyKey: '', gymSig: '', upgSig: '', log: [], rows: [], modalFn: null, lastNoBalls: 0 };

export const state = () => S;
export function replaceState(ns) { S = ns; ui.teamDirty = true; ui.upgSig = ''; ui.gymSig = ''; ui.enemyKey = ''; syncSettings(); renderStatic(); }

// ---------- sonido ----------
const sfx = (() => {
  let ctx = null;
  const tone = (f, t0, d, type = 'square', v = 0.05) => {
    const o = ctx.createOscillator(), g = ctx.createGain();
    o.type = type; o.frequency.value = f; o.connect(g); g.connect(ctx.destination);
    g.gain.setValueAtTime(v, ctx.currentTime + t0); g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + t0 + d);
    o.start(ctx.currentTime + t0); o.stop(ctx.currentTime + t0 + d + 0.02);
  };
  const play = (notes) => {
    if (!S || !S.settings.sound) return;
    try { ctx = ctx || new (window.AudioContext || window.webkitAudioContext)(); if (ctx.state === 'suspended') ctx.resume(); notes.forEach(([f, t, d, ty, v]) => tone(f, t, d, ty, v)); } catch { /* sin audio */ }
  };
  return {
    catch: () => play([[660, 0, 0.1], [880, 0.1, 0.16]]),
    shiny: () => play([[880, 0, 0.1, 'triangle', 0.07], [1175, 0.1, 0.1, 'triangle', 0.07], [1568, 0.2, 0.1, 'triangle', 0.07], [2093, 0.3, 0.3, 'triangle', 0.07]]),
    win: () => play([[523, 0, 0.12], [659, 0.12, 0.12], [784, 0.24, 0.12], [1047, 0.36, 0.35]]),
    lose: () => play([[330, 0, 0.18, 'sawtooth'], [247, 0.18, 0.3, 'sawtooth']]),
    evolve: () => play([[392, 0, 0.1, 'triangle', 0.07], [494, 0.1, 0.1, 'triangle', 0.07], [587, 0.2, 0.1, 'triangle', 0.07], [784, 0.3, 0.3, 'triangle', 0.07]]),
    unlock: () => play([[1000, 0, 0.08, 'triangle'], [1400, 0.08, 0.14, 'triangle']]),
  };
})();

// ---------- avisos ----------
function toast(html, cls = '', img = null) {
  const t = el('div', 'toast ' + cls, (img ? `<img src="${img}" alt="">` : '') + `<div>${html}</div>`);
  const box = $('toasts');
  box.appendChild(t);
  while (box.children.length > 3) box.firstChild.remove();
  setTimeout(() => t.remove(), 3600);
}
function addLog(text, cls = '') {
  ui.log.unshift({ text, cls });
  ui.log.length = Math.min(ui.log.length, 6);
  $('log').innerHTML = ui.log.map((l) => `<li class="${l.cls}">${l.text}</li>`).join('');
}

// ---------- modales ----------
function openModal(html, onBind) {
  $('modalBox').innerHTML = html;
  $('modal').hidden = false;
  if (onBind) onBind($('modalBox'));
}
function closeModal() { $('modal').hidden = true; $('modalBox').innerHTML = ''; ui.modalFn = null; }
const modalOpen = () => !$('modal').hidden;

function confirmBox(title, text, okLabel, onOk, danger = false) {
  openModal(`<h2>${title}</h2><p class="p">${text}</p><div class="actions h"><button class="btn" data-a="no">Cancelar</button><button class="btn ${danger ? 'danger' : 'primary'}" data-a="ok">${okLabel}</button></div>`, (box) => {
    box.querySelector('[data-a=no]').onclick = closeModal;
    box.querySelector('[data-a=ok]').onclick = () => { closeModal(); onOk(); };
  });
}

// ---------- pestañas ----------
function showTab(name) {
  ui.tab = name;
  document.querySelectorAll('.tab').forEach((t) => t.classList.toggle('active', t.id === 'tab-' + name));
  document.querySelectorAll('#tabs button').forEach((b) => b.classList.toggle('on', b.dataset.tab === name));
  if (name === 'team') renderTeam();
  if (name === 'dex') updateDex(true);
  if (name === 'more') renderMore();
  if (name === 'shop') updateShop(true);
}
function bindSeg(segId, prefix, key) {
  $(segId).addEventListener('click', (e) => {
    const b = e.target.closest('button'); if (!b) return;
    ui[key] = b.dataset.sub;
    $(segId).querySelectorAll('button').forEach((x) => x.classList.toggle('on', x === b));
    document.querySelectorAll(`[id^=${prefix}-]`).forEach((s) => s.classList.toggle('on', s.id === `${prefix}-${b.dataset.sub}`));
    if (prefix === 'more') renderMore(); else updateShop(true);
  });
}

// ---------- barra superior ----------
function renderTop() {
  const d = E.derive(S);
  setText($('money'), E.fmt(S.money));
  setText($('dps'), E.fmt(d.dps));
  setText($('clickdmg'), `${E.fmt(d.click)} / toque`);
  const showCandy = S.lifeCandies > 0 || S.candies > 0;
  $('candyBox').hidden = !showCandy;
  if (showCandy) setText($('candies'), E.fmt(S.candies));
}

// ---------- combate ----------
function nextGymKey() {
  for (let i = 0; i < D.GYMS.length; i++) if (!S.badges.includes(i)) return i;
  return S.leagueBeaten ? null : 'league';
}
const gymDef = (k) => (k === 'league' ? D.LEAGUE : D.GYMS[k]);

function renderBattle() {
  const a = E.areaDef(S.area);
  const inGym = S.mode === 'gym';
  setText($('areaName'), E.areaName(S.area));
  setText($('areaSub'), S.area >= D.AREAS.length ? 'Profundidades' : a.sub);
  $('arena').style.setProperty('--h', a.hue);
  toggleCls($('arena'), 'boss', inGym);
  $('areaPrev').disabled = inGym || S.area <= 0;
  $('areaNext').disabled = inGym || !E.areaUnlocked(S, S.area + 1);
  const k = S.kills[S.area] || 0;
  const cleared = !!S.cleared[S.area];
  $('areaProgFill').style.width = (cleared ? 100 : Math.min(100, (k / E.CFG.killsToClear) * 100)) + '%';
  setText($('areaProgText'), cleared ? `Zona despejada · ${E.fmt(k)} derrotados` : `${k} / ${E.CFG.killsToClear} para despejarla`);

  const e = S.enemy;
  const wrap = $('enemyWrap');
  if (e) {
    const key = `${e.id}${e.shiny ? 's' : ''}`;
    if (ui.enemyKey !== key) {
      ui.enemyKey = key;
      $('enemyImg').src = sprite(e.id, e.shiny);
    }
    $('enemyImg').style.visibility = 'visible';
    toggleCls(wrap, 'shiny', !!e.shiny);
    const frac = Math.max(0, e.hp / e.max);
    $('hpFill').style.width = (frac * 100) + '%';
    const hp = $('hpFill').parentElement;
    toggleCls(hp, 'low', frac < 0.25); toggleCls(hp, 'mid', frac >= 0.25 && frac < 0.55);
    setText($('hpText'), `${E.fmt(Math.max(0, e.hp))} / ${E.fmt(e.max)}`);
    const name = e.boss ? e.label : pname(e.id);
    const isNew = !e.boss && !S.dex[e.id];
    setHtml($('enemyName'), `${isNew ? '<img class="new" src="sprites/items/poke-ball.png" alt="Sin registrar" title="Aún no registrado">' : ''}${name}${e.shiny ? ' <span class="star">★</span>' : ''}`);
    $('legendTag').hidden = !e.legend;
  } else {
    $('enemyImg').style.visibility = 'hidden';
    ui.enemyKey = '';
    $('legendTag').hidden = true;
  }

  const lab = $('bossLabel');
  lab.hidden = !inGym;
  if (inGym) {
    const g = S.gym.def;
    setText(lab, `${g.leader === 'Liga Pokémon' ? 'Liga Pokémon' : 'Gimnasio de ' + g.city + ': ' + g.leader} · ${S.gym.fight + 1}/${g.fights.length}`);
  }
  const tm = $('gymTimer');
  tm.hidden = !inGym;
  if (inGym) {
    const total = E.gymTime(S.gym.def);
    $('gymTimerFill').style.width = Math.max(0, S.gym.time / total * 100) + '%';
    setText($('gymTimerText'), `${Math.max(0, S.gym.time).toFixed(1)} s`);
    toggleCls(tm, 'low', S.gym.time < 8);
  }
  renderGymCta();
  renderBalls();
  $('tip').hidden = !(S.stats.clicks < 40 && E.trainerCount(S) === 0);
}

function gymNeed(key) {
  const g = E.gymEstimate(S, key);
  const def = gymDef(key);
  const needDps = g.hp / (g.time * 0.92);
  return { ...g, needDps, def };
}

function renderGymCta() {
  const box = $('gymCta');
  const key = nextGymKey();
  if (S.mode === 'gym') {
    if (ui.gymSig !== 'in') { ui.gymSig = 'in'; box.hidden = false; box.innerHTML = '<div class="t">Combate de gimnasio en curso</div><button class="btn danger" data-a="leave">Abandonar</button>'; }
    return;
  }
  if (key === null) { box.hidden = true; ui.gymSig = 'none'; return; }
  const avail = E.gymAvailable(S, key);
  const def = gymDef(key);
  const sig = `${key}-${avail}-${avail ? '' : (S.cleared[def.after] ? 1 : 0) + '-' + S.badges.length}`;
  if (ui.gymSig !== sig) {
    ui.gymSig = sig; box.hidden = false;
    if (avail) {
      box.innerHTML = `<div class="t">${key === 'league' ? 'Liga Pokémon · ' + def.city : def.city + ': ' + def.leader}</div><div class="need"></div>
        <button class="btn primary" data-a="gym" data-k="${key}">Retar${key === 'league' ? ' a la Liga' : ' a ' + def.leader}</button>`;
    } else {
      const need = key === 'league' && S.badges.length < 8 ? 'Consigue las 8 medallas.' : `Despeja ${E.areaName(def.after)}.`;
      box.innerHTML = `<div class="t">Próximo reto: ${key === 'league' ? 'Liga Pokémon' : def.leader}</div><div class="need">${need}</div>`;
    }
  }
  if (avail) {
    const n = gymNeed(key), nd = box.querySelector('.need');
    setText(nd, `Necesitas ~${E.fmt(n.needDps)} de daño por segundo en ${Math.round(n.time)} s. Tienes ${E.fmt(E.derive(S).dps)}.`);
    toggleCls(nd, 'ok', n.ok); toggleCls(nd, 'no', !n.ok);
  }
}

let ballSig = '';
function renderBalls() {
  const box = $('balls');
  const kids = box.children;
  if (!kids.length) {
    for (const b of D.BALLS) {
      const x = el('button', 'ball', `<img src="sprites/items/${b.icon}.png" alt=""><span>${b.name.replace(' Ball', '')}</span><b></b>`);
      x.dataset.ball = b.id; box.appendChild(x);
    }
  }
  for (const x of kids) {
    const id = x.dataset.ball;
    const info = x.querySelector('b');
    toggleCls(x, 'on', S.ball === id);
    if (id === 'master') { setText(info, `x${S.masterBalls}`); toggleCls(x, 'off', S.masterBalls < 1); }
    else { const c = E.ballCost(S, id); setText(info, `₽${E.fmt(c)}`); toggleCls(x, 'off', S.money < c); }
  }
}

// ---------- equipo ----------
function renderTeam() {
  ui.teamDirty = false;
  const d = E.derive(S);
  $('teamHead').innerHTML = `<div class="card-title">Tu equipo <small>${d.slots}/6 plazas</small></div>
    <div class="p">Poder del equipo: <b>${E.fmt(d.power)}</b> · Multiplica a tus entrenadores y toques por <b>x${E.fmt(d.teamMult)}</b></div>
    <div class="p">Nivel máximo ahora: <b>${E.levelCap(S)}</b> (sube con cada medalla). Ganan EXP al derrotar Pokémon.</div>`;
  const slots = $('teamSlots'); slots.innerHTML = '';
  for (let i = 0; i < 6; i++) {
    if (i >= d.slots) {
      const need = (i - 1) * 2;
      slots.appendChild(el('div', 'slot locked', `<div>Bloqueado</div><small>${need} medallas</small>`));
      continue;
    }
    const id = S.team[i];
    if (!id || !S.owned[id] || S.owned[id].gone) {
      const s = el('button', 'slot empty', '<div>Vacío</div><small>Toca para elegir</small>');
      s.dataset.slot = i; slots.appendChild(s); continue;
    }
    const o = S.owned[id];
    const s = el('button', 'slot', `${o.shiny ? '<span class="shiny-mark">★</span>' : ''}${E.canEvolve(S, id) ? '<span class="evo-mark">EVOLUCIONA</span>' : ''}
      <img src="${sprite(id, o.shiny)}" alt=""><div class="nm">${pname(id)}</div><div class="lv"></div><div class="bar"><i></i></div><div class="lv dd"></div>`);
    s.dataset.poke = id; s.dataset.slot = i; slots.appendChild(s);
  }
  // caja
  const box = $('box'); box.innerHTML = '';
  const list = Object.keys(S.owned).map(Number).filter((id) => !S.owned[id].gone).sort((a, b) => E.pokePowerOf(S, b) - E.pokePowerOf(S, a));
  $('boxCount').textContent = `${list.length} Pokémon`;
  for (const id of list) {
    const o = S.owned[id];
    const x = el('button', `bx${S.team.includes(id) ? ' inteam' : ''}${o.shiny ? ' shiny' : ''}`, `<img src="${sprite(id, o.shiny)}" alt=""><div>${pname(id)}${o.shiny ? ' ★' : ''}</div><div class="lv">Nv. ${o.lvl}</div>`);
    x.dataset.poke = id; box.appendChild(x);
  }
  updateTeam();
}
function updateTeam() {
  const slots = $('teamSlots').children;
  const cap = E.levelCap(S);
  for (const s of slots) {
    const id = s.dataset.poke; if (!id) continue;
    const o = S.owned[id]; if (!o) continue;
    const lv = s.querySelectorAll('.lv');
    setText(lv[0], `Nv. ${o.lvl}${o.lvl >= cap ? ' (máx.)' : ''}`);
    s.querySelector('.bar i').style.width = (o.lvl >= cap ? 100 : (o.xp / E.xpNeed(o.lvl)) * 100) + '%';
    setText(lv[1], `Poder ${E.fmt(E.pokePowerOf(S, id))}`);
  }
}
function evoReady() {
  for (const id in S.owned) if (E.canEvolve(S, +id)) return true;
  return false;
}

function whereFound(id) {
  const out = [];
  D.AREAS.forEach((a, i) => { if (a.pool.some(([p]) => p === id)) out.push(a.name); });
  return out;
}
function evolvesFrom(id) {
  for (const k in D.POKEMON) {
    const evo = D.POKEMON[k].evo; if (!evo) continue;
    const to = Array.isArray(evo[0]) ? evo[0] : [evo[0]];
    if (to.includes(id)) return +k;
  }
  return null;
}

function openPoke(id) {
  const o = S.owned[id]; if (!o) return;
  const sp = D.POKEMON[id], cap = E.levelCap(S);
  const evo = sp.evo;
  let evoHtml = '';
  if (evo && !o.gone) {
    const targets = Array.isArray(evo[0]) ? evo[0] : [evo[0]];
    if (evo[1] === 0) {
      evoHtml = `<p class="p">Evoluciona con una <b>Piedra Evolutiva</b> (tienes ${S.stones}; se compran en Mejoras → Tienda).</p>`;
    } else evoHtml = `<p class="p">Evoluciona a <b>${pname(targets[0])}</b> al nivel <b>${evo[1]}</b>${S.settings.autoEvolve ? ' (automático)' : ''}.</p>`;
    evoHtml += `<div class="actions">${targets.map((t) => `<button class="btn primary" data-evo="${t}" ${E.canEvolve(S, id) ? '' : 'disabled'}>Evolucionar a ${pname(t)}${D.EEVEE_STONES[t] && targets.length > 1 ? ' (' + D.EEVEE_STONES[t] + ')' : ''}</button>`).join('')}</div>`;
  }
  const inTeam = S.team.indexOf(id);
  const slotsN = E.derive(S).slots;
  let teamHtml;
  if (inTeam >= 0 && inTeam < slotsN) teamHtml = `<button class="btn" data-team="remove">Quitar del equipo</button>`;
  else {
    const free = [...Array(slotsN).keys()].find((i) => !S.team[i] || !S.owned[S.team[i]] || S.owned[S.team[i]].gone);
    teamHtml = free !== undefined
      ? `<button class="btn primary" data-team="add" data-slot="${free}">Añadir al equipo</button>`
      : [...Array(slotsN).keys()].map((i) => `<button class="btn" data-team="swap" data-slot="${i}">Cambiar por ${pname(S.team[i])}</button>`).join('');
  }
  openModal(`<img class="sprite-big" src="${sprite(id, o.shiny)}" alt="">
    <h2 class="center">${pname(id)}${o.shiny ? ' <span style="color:var(--shiny)">★</span>' : ''}</h2>
    <div class="kv"><span>Nivel</span><span>${o.lvl} / ${cap}</span><span>Poder</span><span>${E.fmt(E.pokePowerOf(S, id))}</span><span>Stats base</span><span>${sp.bst}</span></div>
    ${o.gone ? '<p class="p">Ha evolucionado: ya no se puede usar.</p>' : evoHtml}
    ${o.gone ? '' : `<div class="actions">${teamHtml}</div>`}
    <div class="actions"><button class="btn" data-a="close">Cerrar</button></div>`, (box) => {
    box.onclick = (e) => {
      const b = e.target.closest('button'); if (!b) return;
      if (b.dataset.a === 'close') return closeModal();
      if (b.dataset.evo) { if (E.evolve(S, id, +b.dataset.evo)) { closeModal(); ui.teamDirty = true; } return; }
      if (b.dataset.team === 'remove') { E.setTeamSlot(S, inTeam, null); }
      else if (b.dataset.team) { E.setTeamSlot(S, +b.dataset.slot, id); }
      else return;
      closeModal(); ui.teamDirty = true; renderTeam();
    };
  });
}

function openPicker(slot) {
  const used = new Set(S.team);
  const list = Object.keys(S.owned).map(Number).filter((id) => !S.owned[id].gone && !used.has(id)).sort((a, b) => E.pokePowerOf(S, b) - E.pokePowerOf(S, a));
  openModal(`<h2>Elegir Pokémon</h2><div class="box" style="max-height:55dvh;overflow:auto">${list.map((id) => `<button class="bx${S.owned[id].shiny ? ' shiny' : ''}" data-pick="${id}"><img src="${sprite(id, S.owned[id].shiny)}" alt=""><div>${pname(id)}</div><div class="lv">Nv. ${S.owned[id].lvl}</div></button>`).join('') || '<p class="p">No tienes más Pokémon libres.</p>'}</div>
    <div class="actions"><button class="btn" data-a="close">Cerrar</button></div>`, (box) => {
    box.onclick = (e) => {
      const b = e.target.closest('button'); if (!b) return;
      if (b.dataset.a === 'close') return closeModal();
      if (b.dataset.pick) { E.setTeamSlot(S, slot, +b.dataset.pick); closeModal(); ui.teamDirty = true; renderTeam(); }
    };
  });
}

// ---------- tienda ----------
function buildTrainers() {
  const list = $('trainerList'); list.innerHTML = ''; ui.rows = [];
  D.TRAINERS.forEach((t, i) => {
    const row = el('div', 'row', `<div class="ico">${i + 1}</div><div class="info"><b></b><small class="d"></small><small class="m"></small></div><button class="buy"></button>`);
    row.dataset.i = i; list.appendChild(row);
    ui.rows.push({ row, ico: row.querySelector('.ico'), name: row.querySelector('b'), d: row.querySelector('.d'), m: row.querySelector('.m'), btn: row.querySelector('.buy') });
  });
}
function updateTrainers() {
  const d = E.derive(S);
  const mult = S.settings.buyMult;
  document.querySelectorAll('#buyMult button').forEach((b) => toggleCls(b, 'on', b.dataset.m === String(mult)));
  D.TRAINERS.forEach((t, i) => {
    const r = ui.rows[i];
    const open = E.trainerUnlocked(S, i);
    const n = S.trainers[t.id] || 0;
    toggleCls(r.row, 'locked', !open);
    if (!open) { setText(r.name, '???'); setText(r.d, 'Sigue avanzando para desbloquearlo.'); setText(r.m, ''); setText(r.btn, ''); r.btn.disabled = true; return; }
    setHtml(r.name, `${t.name} <small>x${n}</small>`);
    const each = t.dps * E.milestoneMult(n) * d.trainerMult * d.teamMult * d.global;
    setText(r.d, `${t.desc} Cada uno: ${E.fmt(each)} DPS.`);
    const nm = E.nextMilestone(n);
    setText(r.m, nm ? `Al llegar a ${nm}: producción x2.` : 'Todos los hitos conseguidos.');
    let k = mult === 'max' ? Math.max(1, E.trainerMax(S, t.id)) : mult;
    const cost = E.trainerCost(S, t.id, k);
    setHtml(r.btn, `₽${E.fmt(cost)}<small>comprar x${k}</small>`);
    r.btn.disabled = S.money < cost;
  });
}

function updateUpgrades(force) {
  const box = $('upgradeList');
  const vis = D.UPGRADES.filter((u) => !S.upg[u.id] && E.upgradeVisible(S, u));
  const sig = vis.map((u) => u.id).join() + '|' + D.UPGRADES.filter((u) => S.upg[u.id]).length;
  if (force || sig !== ui.upgSig) {
    ui.upgSig = sig;
    let html = '<div class="hint">Mejoras de toque (se pueden comprar muchas veces)</div>';
    for (const u of D.CLICK_UPGRADES) html += `<div class="row" data-cu="${u.id}"><div class="ico">${u.id === 'glove' ? '+' : '%'}</div><div class="info"><b>${u.name} <small class="lvl"></small></b><small class="eff"></small></div><button class="buy"></button></div>`;
    html += '<div class="hint" style="padding-top:14px">Mejoras únicas</div>';
    html += vis.length ? vis.map((u) => `<div class="row" data-u="${u.id}"><div class="ico">${u.icon ? `<img src="sprites/items/${u.icon}.png" alt="">` : '★'}</div><div class="info"><b>${u.name}</b><small>${u.desc}</small></div><button class="buy"></button></div>`).join('') : '<div class="hint">Nada por ahora. Aparecen más al desbloquear zonas.</div>';
    box.innerHTML = html;
  }
  for (const u of D.CLICK_UPGRADES) {
    const row = box.querySelector(`[data-cu=${u.id}]`); if (!row) continue;
    const lv = S.clickLvl[u.id] || 0;
    setText(row.querySelector('.lvl'), `Nv. ${lv}${u.max ? '/' + u.max : ''}`);
    const d = E.derive(S);
    setText(row.querySelector('.eff'), u.id === 'glove' ? `Daño base por toque: ${E.fmt(E.baseClick(lv))} (siguiente: ${E.fmt(E.baseClick(lv + 1))})` : `Cada toque suma el ${lv}% de tu DPS (${E.fmt(d.dps * E.CFG.techPct * lv)})`);
    const btn = row.querySelector('.buy');
    if (u.max && lv >= u.max) { setText(btn, 'Máximo'); btn.disabled = true; }
    else { const c = E.clickUpgCost(S, u.id); setText(btn, `₽${E.fmt(c)}`); btn.disabled = S.money < c; }
  }
  for (const u of vis) {
    const row = box.querySelector(`[data-u=${u.id}]`); if (!row) continue;
    const c = E.upgradeCost(u); const btn = row.querySelector('.buy');
    setText(btn, `₽${E.fmt(c)}`); btn.disabled = S.money < c;
  }
}

function updateStore(force) {
  const box = $('storeList');
  if (force || !box.firstChild) {
    box.innerHTML = `<div class="row" data-st="stone"><div class="ico"><img src="sprites/items/moon-stone.png" alt=""></div><div class="info"><b>Piedra Evolutiva <small class="have"></small></b><small>Hace evolucionar a los Pokémon que lo necesitan (Pikachu, Eevee, Vulpix...).</small></div><button class="buy"></button></div>
      <div class="row" data-st="master" hidden><div class="ico"><img src="sprites/items/master-ball.png" alt=""></div><div class="info"><b>Master Ball <small class="have"></small></b><small>Captura segura de un legendario. Se compra con Caramelos Raros.</small></div><button class="buy"></button></div>
      <div class="hint" style="padding-top:12px">Las Poké Balls se pagan solas al intentar capturar. Elige la bola en la pestaña Combate: las mejores capturan más, pero cuestan más.</div>`;
  }
  const st = box.querySelector('[data-st=stone]');
  setText(st.querySelector('.have'), `x${S.stones}`);
  const price = E.stonePrice(S); const b = st.querySelector('.buy');
  setText(b, `₽${E.fmt(price)}`); b.disabled = S.money < price;
  const m = box.querySelector('[data-st=master]');
  m.hidden = !(S.lifeCandies > 0);
  if (!m.hidden) {
    setText(m.querySelector('.have'), `x${S.masterBalls}`);
    const mb = m.querySelector('.buy'); setHtml(mb, `${D.MASTER_BALL_CANDY_COST}<small>caramelos</small>`); mb.disabled = S.candies < D.MASTER_BALL_CANDY_COST;
  }
}
function updateShop(force) {
  if (ui.shopSub === 'trainers') updateTrainers();
  else if (ui.shopSub === 'upgrades') updateUpgrades(force);
  else updateStore(force);
}

// ---------- pokédex ----------
function buildDex() {
  const g = $('dexGrid'); g.innerHTML = '';
  for (let id = 1; id <= D.DEX_SIZE; id++) {
    const c = el('button', 'dc unk', `<img src="${sprite(id, false)}" alt="" loading="lazy"><small>${String(id).padStart(3, '0')}</small>`);
    c.dataset.dex = id; g.appendChild(c);
  }
}
function updateDex(force) {
  const n = E.dexCount(S), sh = E.shinyCount(S);
  const bonus = E.CFG.dexBonus * n + E.CFG.shinyBonus * sh;
  setHtml($('dexHead'), `<div class="card-title">Pokédex de Kanto <small>${n} / ${D.DEX_SIZE}</small></div>
    <div class="p">Shinies: <b>${sh}</b> / ${D.DEX_SIZE} · Bonus de daño por colección: <b>+${Math.round(bonus * 100)}%</b></div>
    <div class="p">Cada Pokémon registrado da +${E.CFG.dexBonus * 100}% de daño y cada shiny otro +${E.CFG.shinyBonus * 100}%.</div>`);
  const cells = $('dexGrid').children;
  for (let i = 0; i < cells.length; i++) {
    const c = cells[i], id = i + 1, st = S.dex[id] || 0;
    const key = st; if (!force && c._st === key) continue; c._st = key;
    c.className = 'dc' + (st ? '' : ' unk') + (st === 2 ? ' sh' : '');
    c.querySelector('img').src = sprite(id, st === 2);
    const old = c.querySelector('.st'); if (old) old.remove();
    if (st === 2) c.appendChild(el('span', 'st', '★'));
  }
}
function openDex(id) {
  const sp = D.POKEMON[id], st = S.dex[id] || 0;
  const found = whereFound(id), from = evolvesFrom(id);
  let how = found.length ? `<b>${found.join(', ')}</b>` : (from ? `Evolucionando a ${st || S.dex[from] ? pname(from) : '???'}` : 'No aparece en estado salvaje');
  if (from && found.length) how += `. También evolucionando a ${S.dex[from] ? pname(from) : '???'}`;
  if (id === 151) how += '. Solo aparece tras reiniciar la aventura al menos una vez.';
  openModal(`<img class="sprite-big" src="${sprite(id, st === 2)}" style="${st ? '' : 'filter:brightness(0) opacity(.3)'}" alt="">
    <h2 class="center">#${String(id).padStart(3, '0')} ${st ? sp.name : '???'}${st === 2 ? ' <span style="color:var(--shiny)">★</span>' : ''}</h2>
    <div class="kv"><span>Estado</span><span>${st === 2 ? 'Registrado (shiny)' : st ? 'Registrado' : 'Sin registrar'}</span>
      <span>Stats base</span><span>${st ? sp.bst : '???'}</span>
      <span>Dificultad de captura</span><span>${sp.legendary ? 'Legendario' : sp.catchRate >= 190 ? 'Fácil' : sp.catchRate >= 90 ? 'Media' : 'Difícil'}</span>
      <span>Dónde</span><span>${how}</span></div>
    ${S.owned[id] && !S.owned[id].gone ? `<div class="actions"><button class="btn primary" data-a="open">Ver mi ${sp.name}</button></div>` : ''}
    <div class="actions"><button class="btn" data-a="close">Cerrar</button></div>`, (box) => {
    box.onclick = (e) => { const b = e.target.closest('button'); if (!b) return; if (b.dataset.a === 'open') { closeModal(); openPoke(id); } else closeModal(); };
  });
}

// ---------- más ----------
function renderMore() {
  const sub = ui.moreSub;
  if (sub === 'gyms') renderGyms(true);
  else if (sub === 'ach') renderAch();
  else if (sub === 'reset') renderReset();
  else renderSettings();
}
function gymStates() {
  return [...D.GYMS.keys(), 'league'].map((k) => `${k}:${(k === 'league' ? S.leagueBeaten : S.badges.includes(k)) ? 'w' : E.gymAvailable(S, k) ? 'a' : 'l'}`).join();
}
function renderGyms(force) {
  const box = $('more-gyms');
  const sig = gymStates();
  if (!force && box._sig === sig) {
    // mismo estado: solo se refresca el texto de "necesitas X DPS"
    box.querySelectorAll('[data-need]').forEach((n) => { const k = n.dataset.need === 'league' ? 'league' : +n.dataset.need; setText(n, `Necesitas ~${E.fmt(gymNeed(k).needDps)} DPS · tienes ${E.fmt(E.derive(S).dps)}`); });
    return;
  }
  box._sig = sig;
  let html = '<div class="card"><div class="card-title">Medallas <small>' + Math.min(8, S.badges.length) + ' / 8</small></div><div class="badges">';
  D.GYMS.forEach((g, i) => { html += `<div class="badge ${S.badges.includes(i) ? 'on' : ''}" style="--c:${g.color}"><i></i>${g.badge.replace('Medalla ', '')}</div>`; });
  html += '</div></div><div class="list" style="margin-top:12px">';
  for (const k of [...D.GYMS.keys(), 'league']) {
    const g = gymDef(k);
    const won = k === 'league' ? S.leagueBeaten : S.badges.includes(k);
    const avail = E.gymAvailable(S, k);
    let info, btn = '';
    if (won) info = `<small class="ok">Superado${k === 'league' ? ': ¡eres el campeón!' : ''}</small>`;
    else if (avail) { info = `<small data-need="${k}"></small>`; btn = `<button class="buy" data-gym="${k}">Retar</button>`; }
    else info = `<small>${k === 'league' ? 'Consigue las 8 medallas y despeja ' + E.areaName(g.after) : 'Despeja ' + E.areaName(g.after)}</small>`;
    html += `<div class="row gymrow ${won ? 'done' : ''}"><div class="ico" style="color:${g.color}">${k === 'league' ? 'L' : +k + 1}</div><div class="info"><b>${k === 'league' ? 'Liga Pokémon' : g.leader}</b><small>${g.city}${k === 'league' ? '' : ' · ' + g.badge}</small>${info}</div>${btn}</div>`;
  }
  box.innerHTML = html + '</div>';
  renderGyms(false);
}
function renderAch() {
  const box = $('more-ach');
  const n = Object.keys(S.ach).length;
  let html = `<div class="card"><div class="card-title">Logros <small>${n} / ${D.ACHIEVEMENTS.length}</small></div><div class="p">Cada logro da <b>+${D.ACHIEVEMENT_BONUS * 100}%</b> de daño. Ahora: +${Math.round(n * D.ACHIEVEMENT_BONUS * 100)}%.</div></div><div class="list" style="margin-top:12px">`;
  for (const a of D.ACHIEVEMENTS) {
    const done = !!S.ach[a.id];
    html += `<div class="row ach ${done ? 'done' : 'todo'}"><div class="ico">${done ? '✓' : '·'}</div><div class="info"><b>${a.name}</b><small>${a.desc}</small></div></div>`;
  }
  box.innerHTML = html + '</div>';
}
function renderReset() {
  const box = $('more-reset');
  const gain = E.candyGain(S);
  const mult = 1 + E.CFG.candyDmg * S.lifeCandies;
  let html = `<div class="card"><div class="card-title">Nueva aventura</div>
    <p class="p">Empiezas de cero en Pueblo Paleta (pierdes ₽, entrenadores, mejoras, medallas y niveles) pero <b>conservas tu Pokédex, shinies, logros y mejoras permanentes</b>.</p>
    <p class="p">A cambio recibes <b>Caramelos Raros</b>: cada uno que consigas da <b>+${E.CFG.candyDmg * 100}%</b> de daño para siempre y sirven para comprar mejoras permanentes.</p>
    <p class="p">Dinero ganado en esta aventura: <b id="rsMoney">₽${E.fmt(S.runMoney)}</b><br>Caramelos al reiniciar ahora: <b id="rsGain" style="color:#ff9ad2">${gain}</b><br>Tienes ${S.lifeCandies} en total (bonus actual x${mult.toFixed(2)}).</p>
    <p class="p">Consejo: sigue bajando pisos de la Cueva Celeste antes de reiniciar. Aparecen más Caramelos cuanto más dinero ganes.</p>
    <div class="actions"><button class="btn primary" id="rsBtn" data-a="prestige" ${gain < 1 ? 'disabled' : ''}>Reiniciar y ganar ${gain} caramelo${gain === 1 ? '' : 's'}</button></div></div>`;
  html += `<div class="card-title pad">Mejoras permanentes <small>Tienes ${S.candies} caramelos</small></div><div class="list">`;
  for (const p of D.PERKS) {
    const own = !!S.perks[p.id];
    html += `<div class="row ${own ? 'done' : ''}"><div class="ico">${p.icon ? `<img src="sprites/items/${p.icon}.png" alt="">` : '★'}</div><div class="info"><b>${p.name}</b><small>${p.desc}</small></div><button class="buy" data-perk="${p.id}" ${own || S.candies < p.cost ? 'disabled' : ''}>${own ? 'Comprada' : p.cost + '<small>caramelos</small>'}</button></div>`;
  }
  box.innerHTML = html + '</div>';
}
function updateReset() {
  const gain = E.candyGain(S);
  const m = $('rsMoney'), g = $('rsGain'), b = $('rsBtn');
  if (!m) return;
  setText(m, `₽${E.fmt(S.runMoney)}`); setText(g, String(gain));
  setText(b, `Reiniciar y ganar ${gain} caramelo${gain === 1 ? '' : 's'}`); b.disabled = gain < 1;
}
function renderSettings() {
  const box = $('more-set');
  const st = S.settings;
  const t = S.stats;
  box.innerHTML = `<div class="card"><div class="card-title">Ajustes</div><div class="toggles" style="flex-direction:column;margin-top:0">
      <label class="toggle"><input type="checkbox" data-set="sound" ${st.sound ? 'checked' : ''}><span>Sonido</span></label>
      <label class="toggle"><input type="checkbox" data-set="wake" ${st.wake ? 'checked' : ''}><span>Mantener la pantalla encendida</span></label>
      <label class="toggle"><input type="checkbox" data-set="autoEvolve" ${st.autoEvolve ? 'checked' : ''}><span>Evolución automática por nivel</span></label>
    </div></div>
    <div class="card"><div class="card-title">Partida</div>
      <div class="actions h"><button class="btn" data-a="export">Exportar</button><button class="btn" data-a="import">Importar</button></div>
      <div class="actions"><button class="btn danger" data-a="wipe">Borrar partida</button></div></div>
    <div class="card"><div class="card-title">Estadísticas</div>
      <div class="kv"><span>Tiempo jugado</span><span>${E.fmtTime(t.playTime)}</span><span>Toques</span><span>${E.fmt(t.clicks)}</span><span>Derrotados</span><span>${E.fmt(t.kills)}</span>
      <span>Capturados</span><span>${E.fmt(t.caught)}</span><span>Shinies</span><span>${t.shinies}</span><span>Evoluciones</span><span>${t.evolved}</span>
      <span>₽ ganados (total)</span><span>${E.fmt(t.lifeMoney)}</span><span>Reinicios</span><span>${S.prestiges}</span></div></div>
    <div class="card"><div class="card-title">Acerca de</div>
      <p class="p">Kanto Idle es un juego de fans, sin ánimo de lucro y sin relación con Nintendo, Game Freak ni The Pokémon Company. Pokémon y sus nombres son marcas de sus propietarios. Sprites de <a style="color:var(--blue)" href="https://github.com/PokeAPI/sprites" target="_blank" rel="noopener">PokeAPI/sprites</a>.</p>
      <p class="p">Sin conexión, tus entrenadores y Pokémon siguen luchando al ${S.perks.p_away ? 80 : 50}% de eficacia durante un máximo de 8 horas (no capturan).</p></div>`;
}

function showExport() {
  const code = E.exportSave(S);
  openModal(`<h2>Exportar partida</h2><p class="p">Copia este código y guárdalo donde quieras. Sirve para pasar la partida a otro dispositivo.</p><textarea id="expTa" readonly>${code}</textarea>
    <div class="actions h"><button class="btn primary" data-a="copy">Copiar</button><button class="btn" data-a="close">Cerrar</button></div>`, (box) => {
    box.onclick = async (e) => {
      const b = e.target.closest('button'); if (!b) return;
      if (b.dataset.a === 'close') return closeModal();
      const ta = $('expTa'); ta.select();
      try { await navigator.clipboard.writeText(code); b.textContent = 'Copiado'; } catch { document.execCommand && document.execCommand('copy'); b.textContent = 'Copiado'; }
    };
  });
}
function showImport() {
  openModal(`<h2>Importar partida</h2><p class="p">Pega aquí el código exportado. Sustituirá a tu partida actual.</p><textarea id="impTa" placeholder="Pega el código aquí"></textarea><p class="p" id="impErr" style="color:#ff9a9a"></p>
    <div class="actions h"><button class="btn primary" data-a="go">Importar</button><button class="btn" data-a="close">Cancelar</button></div>`, (box) => {
    box.onclick = (e) => {
      const b = e.target.closest('button'); if (!b) return;
      if (b.dataset.a === 'close') return closeModal();
      try { const ns = E.importSave($('impTa').value); replaceState(ns); E.save(S); closeModal(); toast('Partida importada', 'good'); showTab('battle'); }
      catch { $('impErr').textContent = 'El código no es válido.'; }
    };
  });
}

// ---------- eventos del motor ----------
function bindEngine() {
  E.onEvent((type, d) => {
    if (!S) return;
    switch (type) {
      case 'catch': {
        const n = pname(d.id);
        if (d.shiny) { addLog(`¡Has capturado a un ${n} shiny!`, 'shiny'); toast(`¡<b>${n} shiny</b> capturado!`, 'shiny', sprite(d.id, true)); sfx.shiny(); }
        else if (d.legend) { addLog(`¡Has capturado al legendario ${n}!`, 'legend'); toast(`¡Has capturado a <b>${n}</b>!`, 'legend', sprite(d.id)); sfx.shiny(); }
        else if (d.isNew) { addLog(`Nuevo en la Pokédex: ${n}`, 'good'); toast(`Nuevo: <b>${n}</b>`, 'good', sprite(d.id)); sfx.catch(); }
        navigator.vibrate && (d.shiny || d.legend) && navigator.vibrate([60, 40, 60]);
        ui.teamDirty = true;
        break;
      }
      case 'flee': if (d.shiny || E.dexCount(S) < 151) addLog(`${pname(d.id)}${d.shiny ? ' shiny' : ''} se ha escapado...`, d.shiny ? 'bad' : ''); break;
      case 'shinySeen': addLog(`¡Ha aparecido un ${pname(d.id)} shiny!`, 'shiny'); break;
      case 'evolve': toast(`<b>${pname(d.from)}</b> ha evolucionado a <b>${pname(d.to)}</b>`, 'good', sprite(d.to, S.owned[d.to] && S.owned[d.to].shiny)); addLog(`${pname(d.from)} evolucionó a ${pname(d.to)}`, 'good'); sfx.evolve(); ui.teamDirty = true; break;
      case 'gymWin': {
        const g = gymDef(d.key);
        sfx.win();
        if (d.key === 'league' && d.first) {
          openModal(`<h2 class="center">¡Campeón de la Liga!</h2><p class="p center">Has vencido a los cinco entrenadores. La <b>Cueva Celeste</b> está abierta, con pisos cada vez más profundos y Pokémon legendarios. Y cuando quieras, puedes empezar una nueva aventura con ventajas permanentes.</p><div class="actions"><button class="btn primary" data-a="close">Genial</button></div>`, (b) => { b.onclick = (e) => e.target.closest('button') && closeModal(); });
        } else toast(d.first ? `¡<b>${g.badge}</b> conseguida!` : `Has vencido a <b>${g.leader}</b>`, 'good');
        addLog(d.first ? `¡${g.badge} conseguida!` : `Vences de nuevo a ${g.leader}`, 'good');
        ui.teamDirty = true; ui.gymSig = '';
        break;
      }
      case 'gymFail': toast(`Has perdido contra <b>${gymDef(d.key).leader}</b>. Hazte más fuerte e inténtalo de nuevo.`, 'bad'); addLog('Derrota en el gimnasio: te quedaste sin tiempo', 'bad'); sfx.lose(); ui.gymSig = ''; break;
      case 'gymStart': ui.gymSig = ''; break;
      case 'bossStep': addLog('Siguiente combate...'); break;
      case 'cleared': toast(`Zona despejada: <b>${E.areaName(d.area)}</b>`); addLog(`Zona despejada: ${E.areaName(d.area)}`, 'good'); break;
      case 'area': ui.enemyKey = ''; break;
      case 'ach': { const a = D.ACHIEVEMENTS.find((x) => x.id === d.id); toast(`Logro: <b>${a.name}</b> (+${D.ACHIEVEMENT_BONUS * 100}% daño)`, 'good'); sfx.unlock(); break; }
      case 'noBalls': if (Date.now() - ui.lastNoBalls > 8000) { ui.lastNoBalls = Date.now(); addLog('No tienes ₽ para lanzar una Poké Ball', 'bad'); } break;
      case 'prestige': toast(`Nueva aventura: +${d.gain} caramelos raros`, 'good'); ui.teamDirty = true; ui.upgSig = ''; ui.gymSig = ''; break;
      default: break;
    }
  });
}

// ---------- interacción ----------
function floater(x, y, text) {
  const box = $('floaters');
  if (box.children.length > 14) box.firstChild.remove();
  const f = el('span', 'dmg', text);
  f.style.left = x + 'px'; f.style.top = y + 'px';
  f.style.setProperty('--dx', (Math.random() * 30 - 15) + 'px');
  box.appendChild(f);
  f.addEventListener('animationend', () => f.remove());
}

function bind() {
  const arena = $('arena');
  arena.addEventListener('pointerdown', (e) => {
    e.preventDefault();
    const dmg = E.click(S);
    const r = arena.getBoundingClientRect();
    if (dmg > 0) {
      floater(e.clientX - r.left, e.clientY - r.top - 10, E.fmt(dmg));
      $('enemyImg').animate([{ transform: 'scale(1)' }, { transform: 'scale(.92) translateY(4px)' }, { transform: 'scale(1)' }], { duration: 110 });
    }
  });
  arena.addEventListener('contextmenu', (e) => e.preventDefault());
  document.addEventListener('contextmenu', (e) => e.preventDefault());

  $('areaPrev').onclick = () => E.goArea(S, S.area - 1);
  $('areaNext').onclick = () => E.goArea(S, S.area + 1);
  $('tabs').addEventListener('click', (e) => { const b = e.target.closest('button'); if (b) showTab(b.dataset.tab); });
  bindSeg('shopSeg', 'shop', 'shopSub');
  bindSeg('moreSeg', 'more', 'moreSub');

  $('balls').addEventListener('click', (e) => { const b = e.target.closest('.ball'); if (b) { S.ball = b.dataset.ball; renderBalls(); } });
  $('optNext').onchange = (e) => { S.settings.autoNext = e.target.checked; };
  $('optGym').onchange = (e) => { S.settings.autoGym = e.target.checked; S.settings.autoLeague = e.target.checked; };

  $('gymCta').addEventListener('click', (e) => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.a === 'leave') E.leaveGym(S);
    else if (b.dataset.a === 'gym') { const k = b.dataset.k === 'league' ? 'league' : +b.dataset.k; E.startGym(S, k); }
    ui.gymSig = '';
  });

  $('teamSlots').addEventListener('click', (e) => {
    const s = e.target.closest('.slot'); if (!s) return;
    if (s.dataset.poke) openPoke(+s.dataset.poke); else if (s.dataset.slot !== undefined && !s.classList.contains('locked')) openPicker(+s.dataset.slot);
  });
  $('box').addEventListener('click', (e) => { const b = e.target.closest('.bx'); if (b) openPoke(+b.dataset.poke); });
  $('btnAutoTeam').onclick = () => { E.autoTeam(S); ui.teamDirty = true; renderTeam(); };

  $('buyMult').addEventListener('click', (e) => { const b = e.target.closest('button'); if (!b) return; S.settings.buyMult = b.dataset.m === 'max' ? 'max' : +b.dataset.m; updateTrainers(); });
  $('trainerList').addEventListener('click', (e) => {
    const b = e.target.closest('.buy'); if (!b || b.disabled) return;
    const i = +b.closest('.row').dataset.i;
    E.buyTrainer(S, D.TRAINERS[i].id, S.settings.buyMult);
    updateTrainers(); renderTop();
  });
  $('upgradeList').addEventListener('click', (e) => {
    const b = e.target.closest('.buy'); if (!b || b.disabled) return;
    const row = b.closest('.row');
    if (row.dataset.cu) E.buyClickUpg(S, row.dataset.cu);
    else if (row.dataset.u) { if (E.buyUpgrade(S, row.dataset.u)) sfx.unlock(); }
    updateUpgrades(); renderTop();
  });
  $('storeList').addEventListener('click', (e) => {
    const b = e.target.closest('.buy'); if (!b || b.disabled) return;
    const k = b.closest('.row').dataset.st;
    if (k === 'stone') E.buyStone(S); else if (k === 'master') E.buyMasterBall(S);
    updateStore(); renderTop(); ui.teamDirty = true;
  });
  $('dexGrid').addEventListener('click', (e) => { const c = e.target.closest('.dc'); if (c) openDex(+c.dataset.dex); });

  $('more-gyms').addEventListener('click', (e) => {
    const b = e.target.closest('[data-gym]'); if (!b) return;
    const k = b.dataset.gym === 'league' ? 'league' : +b.dataset.gym;
    if (E.startGym(S, k)) showTab('battle');
  });
  $('more-reset').addEventListener('click', (e) => {
    const b = e.target.closest('button'); if (!b || b.disabled) return;
    if (b.dataset.perk) { if (E.buyPerk(S, b.dataset.perk)) { sfx.unlock(); renderReset(); } return; }
    if (b.dataset.a === 'prestige') {
      const gain = E.candyGain(S);
      confirmBox('¿Empezar una nueva aventura?', `Perderás tu progreso de esta aventura (dinero, entrenadores, medallas, niveles) y recibirás <b>${gain} Caramelos Raros</b>. Tu Pokédex y tus logros se quedan.`, 'Reiniciar', () => { E.prestige(S); E.save(S); showTab('battle'); });
    }
  });
  $('more-set').addEventListener('change', (e) => {
    const k = e.target.dataset.set; if (!k) return;
    S.settings[k] = e.target.checked;
    if (k === 'wake') hooks.wake && hooks.wake(e.target.checked);
    if (k === 'sound' && e.target.checked) sfx.unlock();
  });
  $('more-set').addEventListener('click', (e) => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.a === 'export') showExport();
    else if (b.dataset.a === 'import') showImport();
    else if (b.dataset.a === 'wipe') confirmBox('¿Borrar la partida?', 'Se perderá todo, también la Pokédex y los Caramelos Raros. No se puede deshacer. Exporta antes si quieres una copia.', 'Borrar todo', () => { hooks.wipe && hooks.wipe(); }, true);
  });
  $('modal').addEventListener('click', (e) => { if (e.target === $('modal')) closeModal(); });
}

function syncSettings() {
  $('optNext').checked = !!S.settings.autoNext;
  $('optGym').checked = !!S.settings.autoGym;
}
function renderStatic() {
  buildTrainers();
  updateTrainers();
  updateStore(true);
  updateUpgrades(true);
}

export function showStarter(onPick) {
  openModal(`<h2 class="center">Bienvenido a Kanto</h2><p class="p center">Elige a tu primer compañero. Con él empezará tu aventura: capturarás Pokémon, contratarás entrenadores y te enfrentarás a los líderes de gimnasio. Si cierras el juego, tus Pokémon seguirán luchando mientras no estás.</p>
    <div class="starters">${D.STARTERS.map((id) => `<button data-s="${id}"><img src="${sprite(id)}" alt="">${pname(id)}</button>`).join('')}</div>`, (box) => {
    box.onclick = (e) => { const b = e.target.closest('[data-s]'); if (!b) return; closeModal(); onPick(+b.dataset.s); };
  });
}
export function showWelcomeBack(r) {
  if (!r || !r.kills) return;
  openModal(`<h2 class="center">¡Bienvenido de nuevo!</h2><p class="p center">Has estado fuera ${E.fmtTime(r.seconds)}. Mientras tanto tu equipo ha derrotado a <b>${E.fmt(r.kills)}</b> Pokémon y ha ganado <b>₽${E.fmt(r.money)}</b>.</p><div class="actions"><button class="btn primary" data-a="close">Seguir</button></div>`, (b) => { b.onclick = (e) => e.target.closest('button') && closeModal(); });
}

// ---------- bucle de pintado ----------
let acc = { shop: 0, team: 0, dex: 0, more: 0 };
export function frame(dt) {
  renderTop();
  if (ui.tab === 'battle') renderBattle();
  acc.shop += dt; acc.team += dt; acc.dex += dt; acc.more += dt;
  if (ui.tab === 'shop' && acc.shop > 0.3) { acc.shop = 0; updateShop(false); }
  if (ui.tab === 'team') { if (ui.teamDirty) renderTeam(); else if (acc.team > 0.5) { acc.team = 0; updateTeam(); } }
  if (ui.tab === 'dex' && acc.dex > 1) { acc.dex = 0; updateDex(false); }
  if (ui.tab === 'more' && acc.more > 1) { acc.more = 0; if (ui.moreSub === 'gyms') renderGyms(false); else if (ui.moreSub === 'reset') updateReset(); }
  toggleCls(document.querySelector('#tabs [data-tab=team]'), 'dot', evoReady());
  $('optGymWrap').classList.toggle('disabled', !E.autoGymUnlocked(S));
  $('optGym').disabled = !E.autoGymUnlocked(S);
}

export function init(state, h = {}) {
  S = state; hooks = h;
  bindEngine(); bind(); buildDex(); renderStatic(); syncSettings();
  renderBattle();
}
