// Service Worker Register 
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function () {
    // Absolute path to the service worker, set by base.html via {% static %}.
    // A bare relative path resolves against the current page URL and 404s.
    navigator.serviceWorker.register(window.swUrl || '/static/service-worker.js')
      .then(registration => {
        //console.log('Service Worker is registered', registration);
      })
      .catch(err => {
        console.error('Registration failed:', err);
      });
  });
}