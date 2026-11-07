/* LH Spectral Palette offline cache, build v57-20261107-1308-6b790e */
const CACHE = 'lh-palette-v57-20261107-1308-6b790e';
const SHELL = ['./', 'index.html', 'manifest.webmanifest', 'icons/icon-180.png', 'icons/icon-192.png', 'icons/icon-512.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('lh-palette-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
// Use what's on the iPad straight away; fetch a fresh copy in the background when online (fonts included).
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const ours = url.origin === self.location.origin;
  const fonts = url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com';
  if (!ours && !fonts) return;
  const key = (ours && req.mode === 'navigate') ? 'index.html' : req;
  e.respondWith(caches.open(CACHE).then(async c => {
    const hit = await c.match(key, { ignoreSearch: ours });
    const net = fetch(req).then(r => { if (r && (r.ok || r.type === 'opaque')) c.put(key, r.clone()); return r; }).catch(() => null);
    if (hit) { e.waitUntil(net); return hit; }
    return (await net) || new Response('Offline and not yet saved on this iPad. Open the app once while online.', { status: 503, headers: { 'Content-Type': 'text/plain' } });
  }));
});
