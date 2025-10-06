// Service Worker for 大势所趋风险框架管理台
const CACHE_NAME = 'prevailing-trend-admin-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/static/css/style.css',
  '/static/js/global_capital_flow_map.js',
  '/static/js/global_capital_flow_enhanced.js',
  '/static/js/global_capital_flow.js'
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // 如果缓存中有响应，则返回缓存的版本
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});