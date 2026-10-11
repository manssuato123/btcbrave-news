
const CACHE_NAME = "btcbrave-news-v4";
const CACHE_PREFIX = "btcbrave-news-";

const APP_SHELL = [
  "/",
  "/index.html",
  "/manifest.json"
];

// INSTALA O NOVO SERVICE WORKER
self.addEventListener("install", event => {
  self.skipWaiting();

  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return Promise.allSettled(
        APP_SHELL.map(url => cache.add(url))
      );
    })
  );
});

// ATIVA A NOVA VERSÃO E LIMPA CACHE ANTIGO
self.addEventListener("activate", event => {
  event.waitUntil((async () => {

    const names = await caches.keys();

    await Promise.all(
      names
        .filter(name =>
          name.startsWith(CACHE_PREFIX) &&
          name !== CACHE_NAME
        )
        .map(name => caches.delete(name))
    );

    await self.clients.claim();

  })());
});

// INTERCEPTA AS REQUISIÇÕES DO SITE
self.addEventListener("fetch", event => {

  const req = event.request;

  if (req.method !== "GET") {
    return;
  }

  const url = new URL(req.url);

  // Somente recursos do próprio site
  if (url.origin !== self.location.origin) {
    return;
  }

  const isNews =
    url.pathname.endsWith("/news.json");

  const isApp =
    req.mode === "navigate" ||
    [
      "/",
      "/index.html",
      "/manifest.json"
    ].includes(url.pathname);

  // HTML E NOTÍCIAS:
  // INTERNET PRIMEIRO, CACHE SE ESTIVER OFFLINE
  if (isNews || isApp) {

    event.respondWith((async () => {

      const cache = await caches.open(CACHE_NAME);

      try {

        const response = await fetch(req);

        if (response.ok) {

          await cache.put(
            isNews ? "/news.json" : url.pathname,
            response.clone()
          );

        }

        return response;

      } catch (error) {

        const fallbackKey = isNews
          ? "/news.json"
          : url.pathname;

        const cached =
          await cache.match(fallbackKey) ||
          (
            req.mode === "navigate"
              ? await cache.match("/index.html")
              : null
          );

        if (cached) {
          return cached;
        }

        throw error;

      }

    })());

  }

});
