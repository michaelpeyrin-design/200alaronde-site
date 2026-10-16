(function () {
  'use strict';
  const card = document.querySelector('.article-strava[data-source]');
  if (!card) return;
  const source = card.dataset.source;
  if (!/^content\/articles\/[^/]+\.json$/.test(source)) return;
  function stat(value) {
    if (value === null || value === undefined || String(value).trim() === '') return '';
    const n = Number(String(value).replace(',', '.'));
    return Number.isFinite(n) && n >= 0 ? n.toLocaleString('fr-FR') : '';
  }
  function render(data) {
    const value = String(data.strava_url || '').trim();
    if (!value) { card.hidden = true; return; }
    let url;
    try { url = new URL(value); } catch (_) { return; }
    if (!['http:', 'https:'].includes(url.protocol)) return;
    let match;
    if (['strava.com', 'www.strava.com'].includes(url.hostname)) {
      match = url.pathname.match(/^\/activities\/(\d+)(?:\/flyover)?\/?$/);
      if (!match) return;
      url = new URL('https://www.strava.com/activities/' + match[1]);
    } else if (url.hostname === 'strava-embeds.com') {
      match = url.pathname.match(/^\/activity\/(\d+)\/?$/);
      if (!match) return;
      url = new URL('https://www.strava.com/activities/' + match[1]);
    } else if (url.hostname !== 'strava.app.link' || !/^\/[A-Za-z0-9_-]+\/?$/.test(url.pathname)) return;
    card.hidden = false;
    card.querySelector('.strava-outing-link').href = url.href;
    const list = card.querySelector('.strava-stats');
    const items = [];
    for (const [key, label, unit] of [['strava_distance_km', 'Distance', ' km'], ['strava_elevation_m', 'Dénivelé positif', ' m D+']]) {
      const number = stat(data[key]);
      if (!number) continue;
      const item = document.createElement('div');
      const term = document.createElement('dt'); term.textContent = label;
      const definition = document.createElement('dd'); definition.textContent = number;
      const small = document.createElement('small'); small.textContent = unit;
      definition.appendChild(small); item.append(term, definition); items.push(item);
    }
    list.replaceChildren(...items); list.hidden = items.length === 0;
  }
  function read(url) { return fetch(url, {cache: 'no-store'}).then(r => {if (!r.ok) throw new Error('HTTP ' + r.status); return r.json();}); }
  const path = source.split('/').map(encodeURIComponent).join('/');
  read('https://raw.githubusercontent.com/michaelpeyrin-design/200alaronde-site/main/' + path + '?v=' + Date.now())
    .catch(() => read('/' + path + '?v=' + Date.now()))
    .then(render).catch(() => {});
})();
