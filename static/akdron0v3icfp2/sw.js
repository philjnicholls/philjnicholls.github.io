// Generated at build time.
const CACHE = 'desert-dash-909c428f0380';
const FILES = ["./","he/","assets/index-DBwDYTJA.js","assets/background-BmMykq4s.js","assets/game-Csu8IN6f.js","assets/gate-CE_r39KU.js","index.html","he/index.html","he/manifest.webmanifest","icons/apple-touch-icon.png","icons/icon-192.png","icons/icon-512.png","icons/maskable-512.png","manifest.webmanifest"];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  if (req.mode === 'navigate') {
    // Offline, serve the cached page for this address (English or Hebrew), else the English one.
    e.respondWith(fetch(req).catch(() => caches.match(req, { ignoreSearch: true }).then((hit) => hit || caches.match('./'))));
    return;
  }
  e.respondWith(caches.match(req, { ignoreSearch: true }).then((hit) => hit || fetch(req)));
});
