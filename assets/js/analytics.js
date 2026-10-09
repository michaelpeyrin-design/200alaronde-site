(function () {
  'use strict';
  var id = 'G-T1D8SY15XN', key = '200alaronde-ga-consent-v1', loaded = false;
  window['ga-disable-' + id] = true;
  function readChoice() {
    try { var v = JSON.parse(localStorage.getItem(key)); return v && Date.now() - v.date < 180 * 86400000 ? v.choice : null; } catch (_) { return null; }
  }
  function start() {
    window['ga-disable-' + id] = false;
    if (loaded) return;
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', id);
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + id;
    document.head.appendChild(script);
  }
  function removeCookies() {
    document.cookie.split(';').forEach(function (part) {
      var name = part.split('=')[0].trim();
      if (!/^_ga(?:_|$)/.test(name)) return;
      ['', location.hostname, '.' + location.hostname, '.200alaronde.fr'].forEach(function (domain) {
        document.cookie = name + '=; Max-Age=0; path=/' + (domain ? '; domain=' + domain : '');
      });
    });
  }
  var style = document.createElement('style');
  style.textContent = '#ga-consent{position:fixed;bottom:0;left:0;right:0;z-index:10000;background:#fff;color:#172b25;padding:20px;box-shadow:0 -2px 15px #0003;font:16px/1.5 system-ui}#ga-consent[hidden]{display:none}#ga-consent p{max-width:900px;margin:0 auto 12px}#ga-consent .ga-actions{display:flex;gap:12px;flex-wrap:wrap;max-width:900px;margin:auto}#ga-consent button{background:#fff;color:#172b25;border:2px solid #285b48;border-radius:6px;padding:10px 20px;font:inherit;cursor:pointer}#ga-settings{display:block;margin:12px auto;padding:8px 12px;background:#fff;color:#172b25;border:1px solid #285b48;border-radius:5px;cursor:pointer}';
  document.head.appendChild(style);
  var banner = document.createElement('section');
  banner.id = 'ga-consent';
  banner.setAttribute('aria-label', 'Choix des cookies de mesure d’audience');
  banner.innerHTML = '<p>Avec votre accord, Google Analytics utilise des cookies pour mesurer les visites et les pages consultées sur 200alaronde.fr. Vous pouvez refuser ou retirer votre accord à tout moment avec « Gestion des cookies ».</p><div class="ga-actions"><button type="button" data-choice="accepted">Accepter</button><button type="button" data-choice="refused">Refuser</button></div>';
  document.body.appendChild(banner);
  banner.addEventListener('click', function (event) {
    var button = event.target.closest('[data-choice]');
    if (!button) return;
    var choice = button.dataset.choice;
    try { localStorage.setItem(key, JSON.stringify({choice: choice, date: Date.now()})); } catch (_) {}
    if (choice === 'accepted') start();
    else { window['ga-disable-' + id] = true; removeCookies(); }
    banner.hidden = true;
    settings.focus();
  });
  var settings = document.createElement('button');
  settings.id = 'ga-settings'; settings.type = 'button'; settings.textContent = 'Gestion des cookies';
  settings.addEventListener('click', function () { banner.hidden = false; banner.querySelector('button').focus(); });
  (document.querySelector('footer') || document.body).appendChild(settings);
  var choice = readChoice();
  banner.hidden = choice === 'accepted' || choice === 'refused';
  if (choice === 'accepted') start();
  document.addEventListener('click', function (event) {
    var a = event.target.closest('a[href]');
    if (!a || !loaded || window['ga-disable-' + id]) return;
    var url; try { url = new URL(a.href); } catch (_) { return; }
    if (url.hostname === 'assoconnect.com' || url.hostname.endsWith('.assoconnect.com')) {
      window.gtag('event', 'clic_inscription', {page_path: location.pathname, transport_type: 'beacon'});
    }
  });
}());
