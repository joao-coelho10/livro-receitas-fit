/* Service worker do Livro de Receitas Fit.
   - App (HTML/CSS/JS/ícones): guardada na instalação; serve da cache e atualiza em segundo plano.
   - recipes.json: rede primeiro (receitas novas aparecem logo), cache se estiver offline.
   - Miniaturas e posters: cache à medida que são vistos.
   - Vídeos: só da cache se tiverem sido guardados (com suporte a pedidos Range), senão rede. */
const VERSION = 'v1';
const SHELL = 'rf-shell-' + VERSION;
const DATA = 'rf-data';
const MEDIA = 'rf-media';
const VIDEOS = 'rf-videos';
const SHELL_FILES = [
  './', 'index.html', 'styles.css', 'app.js', 'manifest.webmanifest',
  'icons/icon-192.png', 'icons/icon-512.png', 'icons/maskable-512.png', 'icons/apple-touch-icon.png', 'icons/favicon-32.png', 'icons/icon.svg',
];

self.addEventListener('install', (e) => {
  e.waitUntil((async () => {
    const c = await caches.open(SHELL);
    await c.addAll(SHELL_FILES.map((u) => new Request(u, { cache: 'reload' })));
    const d = await caches.open(DATA);
    try { await d.add(new Request('recipes.json', { cache: 'reload' })); } catch (err) { /* fica para depois */ }
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    const keep = [SHELL, DATA, MEDIA, VIDEOS];
    for (const k of await caches.keys()) if (k.startsWith('rf-') && !keep.includes(k)) await caches.delete(k);
    await self.clients.claim();
  })());
});

const scopePath = new URL(self.registration.scope).pathname;
const rel = (url) => url.pathname.startsWith(scopePath) ? url.pathname.slice(scopePath.length) : url.pathname;

async function staleWhileRevalidate(req, cacheName, key) {
  const c = await caches.open(cacheName);
  const hit = await c.match(key || req, { ignoreSearch: true });
  const net = fetch(req).then((res) => { if (res && res.ok && res.type !== 'opaque') c.put(key || req, res.clone()); return res; }).catch(() => null);
  if (hit) { net.catch(() => {}); return hit; }
  return (await net) || new Response('Sem ligação', { status: 503, headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}

async function networkFirst(req, cacheName) {
  const c = await caches.open(cacheName);
  try {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), 4000);
    const res = await fetch(req, { signal: ctrl.signal, cache: 'no-cache' });
    clearTimeout(t);
    if (res.ok) await c.put(req.url.split('?')[0], res.clone());
    return res;
  } catch (err) {
    const hit = await c.match(req.url.split('?')[0]);
    if (hit) return hit;
    throw err;
  }
}

async function cacheFirst(req, cacheName) {
  const c = await caches.open(cacheName);
  const hit = await c.match(req, { ignoreSearch: true });
  if (hit) return hit;
  const res = await fetch(req);
  if (res.ok) c.put(req, res.clone());
  return res;
}

async function video(req) {
  const c = await caches.open(VIDEOS);
  const hit = await c.match(req.url.split('?')[0]);
  if (!hit) return fetch(req);
  const range = req.headers.get('range');
  if (!range) return hit;
  const buf = await hit.arrayBuffer();
  const size = buf.byteLength;
  const m = /bytes=(\d*)-(\d*)/.exec(range) || [];
  let start = m[1] ? parseInt(m[1], 10) : 0;
  let end = m[2] ? parseInt(m[2], 10) : size - 1;
  if (!m[1] && m[2]) { start = size - parseInt(m[2], 10); end = size - 1; }
  end = Math.min(end, size - 1);
  if (start >= size || start > end) return new Response(null, { status: 416, headers: { 'Content-Range': 'bytes */' + size } });
  return new Response(buf.slice(start, end + 1), {
    status: 206, statusText: 'Partial Content',
    headers: { 'Content-Type': 'video/mp4', 'Content-Range': `bytes ${start}-${end}/${size}`, 'Content-Length': String(end - start + 1), 'Accept-Ranges': 'bytes' },
  });
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  const p = rel(url);
  if (req.mode === 'navigate') { e.respondWith(staleWhileRevalidate(req, SHELL, 'index.html')); return; }
  if (p === 'recipes.json') { e.respondWith(networkFirst(req, DATA)); return; }
  if (p.startsWith('videos/')) { e.respondWith(video(req)); return; }
  if (p.startsWith('media/')) { e.respondWith(cacheFirst(req, MEDIA)); return; }
  if (p === 'sw.js') return;
  e.respondWith(staleWhileRevalidate(req, SHELL));
});
