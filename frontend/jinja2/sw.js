var cacheName = 'afk-hangzhou-pwa';
var dataCacheName = 'afk-hangzhou-data-v5';
var filesToCache = [
    '/static/css/bootstrap.min.css',
    '/static/css/bootstrap-datepicker.min.css',
    '/static/admin/js/vendor/jquery/jquery.js',
    '/static/js/bootstrap.min.js',
    '/static/js/bootstrap-datepicker.min.js',
    '/static/js/bootstrap-datepicker.zh-CN.min.js',
    '/static/js/echarts.min.js'
]

self.addEventListener('install', function(e) {
  console.log('[ServiceWorker] Install');
  e.waitUntil(
    caches.open(cacheName).then(function(cache) {
      console.log('[ServiceWorker] Caching app shell');
      return cache.addAll(filesToCache);
    })
  );
});
self.addEventListener('activate', function(e) {
  console.log('[ServiceWorker] Activate');
  e.waitUntil(
    caches.keys().then(function(keyList) {
      return Promise.all(keyList.map(function(key) {
        console.log('[ServiceWorker] Removing old cache', key);
        if (key !== cacheName && key !== dataCacheName) {
          return caches.delete(key);
        }
      }));
    })
  );
});

self.addEventListener('fetch', function(e) {
  e.respondWith(
      caches.match(e.request).then(function(response) {
        return response || fetch(e.request);
      })
    );
})
