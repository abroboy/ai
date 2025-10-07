// Service Worker for 大势所趋风险框架管理台
// 缓存版本控制
const CACHE_NAME = 'prevailing-trend-admin-v2';
const DYNAMIC_CACHE_NAME = 'prevailing-trend-dynamic-v2';
const MAX_DYNAMIC_CACHE_SIZE = 50;

// 核心资源预缓存列表
const urlsToCache = [
  '/',
  '/index.html',
  '/static/css/style.css',
  '/static/css/global_capital_flow.css',
  '/static/js/global_capital_flow.js',
  '/static/js/domestic_hotspot_enhanced.js',
  '/static/js/domestic_hotspot_data.js',
  '/static/js/domestic_hotspot_ui.js',
  '/static/js/domestic_hotspot_utils.js',
  '/static/js/missing_modules.js',
  '/static/js/global_capital_flow_map.js',
  '/static/js/global_capital_flow_chart.js',
  '/static/js/global_capital_flow_utils.js'
];

// 安装阶段 - 预缓存核心资源
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Service Worker: 预缓存核心资源');
        // 使用Promise.all和map确保每个请求都正确处理
        return Promise.all(
          urlsToCache.map(url => {
            return fetch(url).then(response => {
              if (response.ok) {
                return cache.put(url, response);
              }
              console.warn(`Service Worker: 预缓存失败: ${url}`);
              return Promise.resolve(); // 即使单个文件失败也继续
            }).catch(error => {
              console.error(`Service Worker: 预缓存错误: ${url}`, error);
              return Promise.resolve(); // 即使单个文件失败也继续
            });
          })
        );
      })
      .then(() => {
        // 强制激活新的Service Worker
        self.skipWaiting();
      })
  );
});

// 激活阶段 - 清理旧缓存
self.addEventListener('activate', function(event) {
  event.waitUntil(
    Promise.all([
      // 清理旧缓存
      caches.keys().then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== CACHE_NAME && cacheName !== DYNAMIC_CACHE_NAME) {
              console.log('Service Worker: 清理旧缓存:', cacheName);
              return caches.delete(cacheName);
            }
            return Promise.resolve();
          })
        );
      }),
      // 确保新的Service Worker接管所有客户端
      self.clients.claim()
    ])
  );
});

// 动态调整动态缓存大小
function trimCache(cacheName, maxItems) {
  caches.open(cacheName)
    .then(cache => {
      cache.keys()
        .then(keys => {
          if (keys.length > maxItems) {
            cache.delete(keys[0])
              .then(() => trimCache(cacheName, maxItems));
          }
        });
    });
}

// 资源请求处理策略
self.addEventListener('fetch', function(event) {
  const requestUrl = new URL(event.request.url);
  
  // 跳过对开发工具和特定API请求的缓存
  if (requestUrl.pathname.includes('/@vite/client') || 
      requestUrl.pathname.includes('/api/') || 
      requestUrl.pathname.includes('/database')) {
    event.respondWith(fetch(event.request));
    return;
  }
  
  // 对不同类型的资源采用不同的缓存策略
  if (requestUrl.pathname.includes('/index.html')) {
    // HTML页面: 网络优先，但有离线回退
    event.respondWith(
      fetch(event.request)
        .then(response => {
          // 更新缓存中的HTML
          const responseClone = response.clone();
          caches.open(CACHE_NAME)
            .then(cache => cache.put('/index.html', responseClone));
          return response;
        })
        .catch(() => {
          // 网络错误时回退到缓存
          return caches.match('/index.html')
            .then(response => response || caches.match('/'));
        })
    );
  } else if (requestUrl.pathname.includes('/static/')) {
    // 静态资源: 缓存优先，定期更新
    event.respondWith(
      caches.match(event.request)
        .then(cacheResponse => {
          // 并行发起网络请求更新缓存
          const fetchPromise = fetch(event.request)
            .then(networkResponse => {
              // 更新动态缓存
              if (networkResponse.ok) {
                const responseClone = networkResponse.clone();
                caches.open(DYNAMIC_CACHE_NAME)
                  .then(cache => {
                    cache.put(event.request, responseClone);
                    // 调整缓存大小
                    trimCache(DYNAMIC_CACHE_NAME, MAX_DYNAMIC_CACHE_SIZE);
                  });
              }
              return networkResponse;
            })
            .catch(() => null); // 网络错误则忽略
          
          // 如果缓存中有响应，直接返回，同时后台更新缓存
          return cacheResponse || fetchPromise;
        })
        .catch(() => {
          // 所有缓存策略失败时的最终回退
          return new Response('网络错误，请检查您的连接', {
            status: 503,
            statusText: 'Service Unavailable',
            headers: { 'Content-Type': 'text/plain' }
          });
        })
    );
  } else if (requestUrl.hostname === 'cdn.jsdelivr.net') {
    // CDN资源: 尝试缓存，但失败则直接从网络获取
    event.respondWith(
      caches.match(event.request)
        .then(cacheResponse => {
          if (cacheResponse) return cacheResponse;
          
          return fetch(event.request)
            .then(networkResponse => {
              if (networkResponse.ok) {
                const responseClone = networkResponse.clone();
                caches.open(DYNAMIC_CACHE_NAME)
                  .then(cache => {
                    cache.put(event.request, responseClone);
                    trimCache(DYNAMIC_CACHE_NAME, MAX_DYNAMIC_CACHE_SIZE);
                  });
              }
              return networkResponse;
            });
        })
    );
  } else {
    // 其他资源: 网络优先
    event.respondWith(fetch(event.request));
  }
});

// 监听消息来自客户端
self.addEventListener('message', function(event) {
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
  }
});

// 添加错误处理
self.addEventListener('error', function(event) {
  console.error('Service Worker 错误:', event.error);
});

self.addEventListener('unhandledrejection', function(event) {
  console.error('Service Worker 未处理的Promise拒绝:', event.reason);
});