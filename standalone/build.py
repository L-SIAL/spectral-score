#!/usr/bin/env python3
"""Build the offline (installable) iPad app from the latest artifact HTML.

Usage:  python3 build.py            (uses the newest ipad/lh-spectral-palette-sketchpad_vNN.html)
        python3 build.py v57         (a specific version)

Writes site/: index.html, manifest.webmanifest, sw.js, icons/.
The artifact file is never changed. Re-run after every new iPad version, then upload site/.
"""
import glob, os, re, sys, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
IPAD = os.path.join(HERE, '..', 'ipad')
SITE = os.path.join(HERE, 'site')

def pick_source():
    files = glob.glob(os.path.join(IPAD, 'lh-spectral-palette-sketchpad_v*.html'))
    def ver(p):
        m = re.search(r'_v(\d+)(?:\.(\d+))?\.html$', p)
        return (int(m.group(1)), int(m.group(2) or 0)) if m else (-1, -1)
    files = [f for f in files if ver(f)[0] >= 0]
    if len(sys.argv) > 1:
        want = sys.argv[1].lstrip('v')
        files = [f for f in files if re.search(r'_v' + re.escape(want) + r'\.html$', f)]
    assert files, 'no matching iPad html found'
    return max(files, key=ver)

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="LH Palette">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#f2ede2">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/icon-180.png">
<link rel="icon" href="icons/icon-192.png">
<style>html,body{margin:0}</style>
</head>
<body>
"""

# Replaces claude.ai's downloads capability: iPad share sheet (Save to Files), else a plain download.
SHIM = r"""
if (!(window.claude && window.claude.use)) downloads = { async save({ filename, data }) {
  const file = new File([data], filename, { type: 'application/json' });
  if (navigator.canShare && navigator.share) {
    let ok = false; try { ok = navigator.canShare({ files: [file] }); } catch (e) { }
    if (ok) {
      try { await navigator.share({ files: [file] }); return; }
      catch (e) { if (e && e.name === 'AbortError') throw { code: 'declined' }; /* otherwise fall through to a download */ }
    }
  }
  const a = document.createElement('a'); a.href = URL.createObjectURL(file); a.download = filename;
  document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 4000);
}, async saveMany(list) {   // several sketches in one share sheet (Save to Files saves them all)
  const files = list.map(({ filename, data }) => new File([data], filename, { type: 'application/json' }));
  let ok = false; try { ok = navigator.canShare && navigator.canShare({ files }); } catch (e) { }
  if (!ok) throw { code: 'unsupported' };
  try { await navigator.share({ files }); } catch (e) { if (e && e.name === 'AbortError') throw { code: 'declined' }; throw e; }
} };
"""

TAIL = """
<script>
/* Standalone build __BUILD__: keep the app on the iPad so it opens with no internet. */
if ('serviceWorker' in navigator) window.addEventListener('load', () => {
  // an update downloads in the background; when it takes over, say so and offer a reload (the open sketch is kept on the iPad)
  const had = !!navigator.serviceWorker.controller;
  let shown = false;
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if (!had || shown) return; shown = true;
    const bar = document.createElement('div');
    bar.setAttribute('role', 'status');
    bar.style.cssText = 'position:fixed;left:50%;bottom:calc(16px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:9999;display:flex;gap:10px;align-items:center;padding:10px 14px;border-radius:10px;background:#3b2a40;color:#fff;font:14px/1.3 -apple-system,system-ui,sans-serif;box-shadow:0 4px 18px rgba(0,0,0,.25);max-width:calc(100vw - 32px)';
    bar.innerHTML = '<span>A new version of the app has downloaded. Save your sketch, then reload to use it.</span>';
    const mk = (t, fn, strong) => { const x = document.createElement('button'); x.textContent = t; x.style.cssText = 'min-height:34px;padding:0 12px;border-radius:7px;border:1px solid #fff6;background:' + (strong ? '#fff;color:#3b2a40' : 'transparent;color:#fff') + ';font:inherit;font-weight:600'; x.onclick = fn; bar.appendChild(x); };
    mk('Reload now', () => location.reload(), true);
    mk('Later', () => bar.remove());
    document.body.appendChild(bar);
  });
  navigator.serviceWorker.register('sw.js').then(r => r.update().catch(() => { })).catch(() => { });
});
</script>
</body>
</html>
"""

SW = """/* LH Spectral Palette offline cache, build __BUILD__ */
const CACHE = 'lh-palette-__BUILD__';
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
"""

MANIFEST = """{
  "name": "LH Spectral Palette",
  "short_name": "LH Palette",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "orientation": "any",
  "background_color": "#ece5d8",
  "theme_color": "#f2ede2",
  "icons": [
    { "src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
"""

def make_icons():
    # Icon: icon-source.png (1024 square, opaque; iOS rounds the corners itself).
    # Current source: "1-sage-diagonal" from spectral-scores-icons (8 Nov 2026).
    from PIL import Image
    os.makedirs(os.path.join(SITE, 'icons'), exist_ok=True)
    im = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon-source.png')).convert('RGB')
    for n in (180, 192, 512):
        im.resize((n, n), Image.LANCZOS).save(os.path.join(SITE, 'icons', f'icon-{n}.png'))

def main():
    src = pick_source()
    html = open(src, encoding='utf-8').read()
    vname = re.search(r'_(v[\d.]+)\.html$', src).group(1)
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M')
    build = f'{vname}-{stamp}-' + hashlib.sha1(html.encode()).hexdigest()[:6]

    anchor = "if (window.claude && window.claude.use) window.claude.use('downloads')"
    i = html.find(anchor)
    assert i >= 0, 'downloads anchor not found: check the save code before building'
    j = html.find('\n', i)
    html = html[:j + 1] + SHIM + html[j + 1:]
    html = html.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    assert '<!doctype' not in html[:200].lower(), 'source already has a document skeleton'

    os.makedirs(SITE, exist_ok=True)
    open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8').write(HEAD + html + TAIL.replace('__BUILD__', build))
    open(os.path.join(SITE, 'sw.js'), 'w', encoding='utf-8').write(SW.replace('__BUILD__', build))
    open(os.path.join(SITE, 'manifest.webmanifest'), 'w', encoding='utf-8').write(MANIFEST)
    open(os.path.join(SITE, '.nojekyll'), 'w').write('')
    make_icons()
    print('built', build, 'from', os.path.basename(src))

if __name__ == '__main__':
    main()
