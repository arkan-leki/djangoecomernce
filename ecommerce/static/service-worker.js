// -----------------------------------------------------------------
// Service worker for the Django + Suha storefront.
//
// IMPORTANT: this worker must NEVER cache Django endpoints. An earlier
// version did `caches.match()` first for every same-origin GET, which
// froze `/cart/fetch/` at its first (empty) response — the cart then
// showed no items forever, even though the server had them.
//
// Rules:
//   - non-GET (cart add/update/delete, logins, admin posts) -> not intercepted
//   - /cart/, /accounts/, /admin/, /payment/, /media/        -> not intercepted
//   - /static/...  -> cache-first (immutable, versioned filenames)
//   - everything else (HTML navigations) -> network-first, cache fallback,
//     then the offline page
// -----------------------------------------------------------------

const staticCacheName = 'precache-django-v2';
const dynamicCacheName = 'runtimecache-django-v2';
const OFFLINE_URL = '/static/offline.html';

// Never touch these: they are dynamic, user-specific or session-bound.
const BYPASS_PREFIXES = ['/cart/', '/accounts/', '/admin/', '/payment/', '/media/'];

// Pre Caching Assets (absolute paths — the worker is served from "/")
const precacheAssets = [
    '/',
    '/static/style.css',
    '/static/css/bootstrap.min.css',
    '/static/css/all.min.css',
    '/static/css/brands.min.css',
    '/static/css/solid.min.css',
    '/static/css/owl.carousel.min.css',
    '/static/css/magnific-popup.css',
    '/static/css/nice-select.css',
    '/static/js/bootstrap.bundle.min.js',
    '/static/js/jquery.min.js',
    '/static/js/alpine.min.js',
    '/static/js/cart.js',
    '/static/js/theme-switching.js',
    '/static/js/active.js',
    '/static/js/no-internet.js',
    '/static/img/core-img/logo-small.png',
    '/static/img/core-img/logo-white.png',
    '/static/img/icons/icon-192x192.png',
    OFFLINE_URL,
];

// Install Event
self.addEventListener('install', function (event) {
    self.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName).then(function (cache) {
            // addAll() rejects the whole install if any single URL 404s,
            // so add them individually and ignore failures.
            return Promise.all(
                precacheAssets.map(function (url) {
                    return cache.add(url).catch(function (err) {
                        console.warn('[sw] precache skipped', url, err);
                    });
                })
            );
        })
    );
});

// Activate Event — drop every cache that isn't the current version, which is
// what purges a cache poisoned by the old worker.
self.addEventListener('activate', function (event) {
    event.waitUntil(
        caches.keys().then(function (keys) {
            return Promise.all(keys
                .filter(function (key) {
                    return key !== staticCacheName && key !== dynamicCacheName;
                })
                .map(function (key) { return caches.delete(key); })
            );
        }).then(function () { return self.clients.claim(); })
    );
});

// Fetch Event
self.addEventListener('fetch', function (event) {
    const request = event.request;

    // 1. Only GETs. Cart POSTs, logins and admin writes must always reach Django.
    if (request.method !== 'GET') return;

    const url = new URL(request.url);

    // 2. Same-origin only.
    if (url.origin !== self.location.origin) return;

    // 3. Dynamic Django endpoints: never intercept, never cache.
    if (BYPASS_PREFIXES.some(function (p) { return url.pathname.indexOf(p) === 0; })) return;

    // 4. The worker script itself is managed by the browser.
    if (url.pathname === '/service-worker.js') return;

    // 5. Static assets: cache-first is safe, filenames are fixed per release.
    if (url.pathname.indexOf('/static/') === 0) {
        event.respondWith(
            caches.match(request).then(function (hit) {
                if (hit) return hit;
                return fetch(request).then(function (response) {
                    if (response && response.status === 200 && response.type === 'basic') {
                        const copy = response.clone();
                        caches.open(dynamicCacheName).then(function (cache) {
                            cache.put(request, copy);
                        });
                    }
                    return response;
                });
            })
        );
        return;
    }

    // 6. HTML navigations: network-first so pages are never stale, with the
    //    cache and then the offline page as fallbacks.
    event.respondWith(
        fetch(request).then(function (response) {
            if (response && response.status === 200 && response.type === 'basic') {
                const copy = response.clone();
                caches.open(dynamicCacheName).then(function (cache) {
                    cache.put(request, copy);
                });
            }
            return response;
        }).catch(function () {
            return caches.match(request).then(function (hit) {
                return hit || caches.match(OFFLINE_URL);
            });
        })
    );
});
