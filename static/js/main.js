// Main JS for Hotel ERP admin UI
(function () {
  'use strict';

  // Feather icons fallback init (base.html also initializes after DOMContentLoaded)
  if (window.feather) {
    try { window.feather.replace(); } catch (e) { /* noop */ }
  }

  // Example: highlight active link in sidebar based on current path
  function setActiveSidebarLink() {
    var links = document.querySelectorAll('#sidebarMenu .nav-link');
    var path = window.location.pathname;
    links.forEach(function (link) {
      try {
        var href = link.getAttribute('href');
        if (!href) return;
        if (href === '/' && path !== '/') return;
        if (path.startsWith(href)) {
          link.classList.add('active');
        } else {
          link.classList.remove('active');
        }
      } catch (_) {}
    });
  }

  // Django CSRF setup for jQuery
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  if (window.jQuery) {
    var csrftoken = getCookie('csrftoken');
    try {
      window.jQuery.ajaxSetup({
        beforeSend: function (xhr, settings) {
          var safeMethod = (/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type));
          if (!safeMethod && !this.crossDomain) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
          }
          xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        }
      });
    } catch (_) {}
  }

  document.addEventListener('DOMContentLoaded', function () {
    setActiveSidebarLink();
  });
})();
