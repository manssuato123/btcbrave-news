const CACHE_NAME = 'btcbrave-news-v2';
const CACHE_PREFIX = 'btcbrave-news-';
const APP_SHELL = ['/', '/index.html', '/manifest.json'];

self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache =>
      Promise.allSettled(APP_SHELL.map(url => cache.add(url)))
    )
  );
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(names
      .filter(name => name.startsWith(CACHE_PREFIX) && name !== CACHE_NAME)
      .map(name => caches.delete(name)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  const isNews = url.pathname.endsWith('/news.json');
  const isApp = req.mode === 'navigate' ||
    ['/index.html', '/manifest.json', '/'].includes(url.pathname);

  // HTML e notícias usam rede primeiro. Em falha de rede, cache offline.
  if (isNews || isApp) {
    event.respondWith((async () => {
      const cache = await caches.open(CACHE_NAME);
      try {
        const response = await fetch(req);
        if (response.ok) {
          await cache.put(isNews ? '/news.json' : url.pathname, response.clone());
        }
        return response;
      } catch (error) {
        const fallbackKey = isNews ? '/news.json' : url.pathname;
        const cached = await cache.match(fallbackKey) ||
          (req.mode === 'navigate' ? await cache.match('/index.html') : null);
        if (cached) return cached;
        throw error;
      }
    })());
  }
});
