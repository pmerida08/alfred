import * as E from './engine.js';
import * as UI from './ui.js';

let S = E.load() || E.newState();
let lastWall = Date.now();
let wakeLock = null;

async function setWake(on) {
  try {
    if (on && 'wakeLock' in navigator && document.visibilityState === 'visible') wakeLock = await navigator.wakeLock.request('screen');
    else if (!on && wakeLock) { await wakeLock.release(); wakeLock = null; }
  } catch { /* el navegador puede denegarlo (ahorro de batería) */ }
}

function boot() {
  UI.init(S, {
    wake: setWake,
    wipe: () => { E.wipe(); location.reload(); },
  });
  if (!S.starter) UI.showStarter((id) => { E.chooseStarter(S, id); E.save(S); });
  else {
    // Progreso mientras el juego estaba cerrado
    const away = (Date.now() - S.last) / 1000;
    UI.showWelcomeBack(E.offline(S, away));
  }
  if (S.settings.wake) setWake(true);
  lastWall = Date.now();
  setInterval(loop, 100);
  setInterval(() => E.save(S), 10000);
}

function loop() {
  S = UI.state();
  const now = Date.now();
  let dt = (now - lastWall) / 1000;
  lastWall = now;
  if (!S.starter) { UI.frame(0.1); return; }
  if (dt > 3) {
    // El navegador congeló la pestaña (pantalla apagada, otra app): se cuenta como tiempo sin conexión
    UI.showWelcomeBack(E.offline(S, dt));
    dt = 0.1;
  }
  while (dt > 0) { const d = Math.min(1, dt); E.tick(S, d); dt -= d; }
  UI.frame(0.1);
}

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'hidden') E.save(S);
  else if (S.settings.wake) setWake(true);
});
addEventListener('pagehide', () => E.save(S));

boot();

if ('serviceWorker' in navigator && location.protocol.startsWith('http')) {
  addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));
}
