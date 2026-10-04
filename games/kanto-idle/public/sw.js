// Service worker: deja el juego instalable y jugable sin conexión.
// Sube VERSION cuando cambies archivos para que los móviles refresquen la caché.
const VERSION = 'kanto-idle-v1';
const CORE = ['./', 'index.html', 'css/style.css', 'js/main.js', 'js/ui.js', 'js/engine.js', 'js/data.js', 'manifest.webmanifest', 'icons/icon-192.png', 'icons/icon-512.png'];

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(VERSION);
    await cache.addAll(CORE);
    // Sprites normales y objetos: uno a uno para que un fallo suelto no tumbe la instalación.
    const extra = [];
    for (let i = 1; i <= 151; i++) extra.push(`sprites/pokemon/${i}.png`);
    for (const n of ['poke-ball', 'great-ball', 'ultra-ball', 'master-ball', 'rare-candy', 'lucky-egg', 'amulet-coin', 'moon-stone', 'shiny-charm', 'exp-share']) extra.push(`sprites/items/${n}.png`);
    await Promise.all(extra.map((u) => cache.add(u).catch(() => {})));
    self.skipWaiting();
  })());
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== VERSION) await caches.delete(k);
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  const isSprite = req.url.includes('/sprites/');
  event.respondWith((async () => {
    const cache = await caches.open(VERSION);
    const hit = await cache.match(req, { ignoreSearch: true });
    // Sprites: caché primero. Código: caché al instante y se refresca en segundo plano.
    const refresh = fetch(req).then((res) => { if (res.ok) cache.put(req, res.clone()); return res; }).catch(() => null);
    if (hit) { if (!isSprite) event.waitUntil(refresh); return hit; }
    const res = await refresh;
    return res || (req.mode === 'navigate' ? cache.match('index.html') : Response.error());
  })());
});
