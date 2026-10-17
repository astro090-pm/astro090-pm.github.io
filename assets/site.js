/* Поиск по сайту и переключение темы. Без зависимостей. */
(() => {
  const root = document.currentScript ? document.currentScript.dataset.root || '' : '';
  const html = document.documentElement;

  // ----- Тема: светлая / тёмная; выбор помнится в браузере, по умолчанию — как в системе
  const themeBtn = document.getElementById('theme-toggle');
  const isDark = () => html.dataset.theme ? html.dataset.theme === 'dark'
    : matchMedia('(prefers-color-scheme: dark)').matches;
  const syncBtn = () => themeBtn && themeBtn.setAttribute('aria-pressed', String(isDark()));
  syncBtn();
  if (themeBtn) themeBtn.addEventListener('click', () => {
    const next = isDark() ? 'light' : 'dark';
    html.dataset.theme = next;
    try { localStorage.setItem('theme', next); } catch (e) {}
    syncBtn();
  });

  // ----- Поиск: окно поверх страницы, ↑↓ навигация, ↵ открыть, esc закрыть, «/» или Ctrl+K — открыть
  const openBtn = document.getElementById('search-open');
  let index = null, dlg, input, list, sel = 0, hits = [];
  const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const EN = document.documentElement.lang === 'en';
  const L = EN ? {dlg:'Site search', ph:'Search: posts, cases, projects…', what:'Search query', hint:'↑↓ navigate · ↵ open · esc close', load:'Loading…', none:'Nothing found', off:'Search unavailable'}
    : {dlg:'Поиск по сайту', ph:'Поиск: посты, кейсы, проекты…', what:'Что ищем', hint:'↑↓ навигация · ↵ открыть · esc закрыть', load:'Загружаю…', none:'Ничего не нашлось', off:'Поиск недоступен'};
  const norm = s => s.toLowerCase().replace(/ё/g, 'е');

  function build() {
    dlg = document.createElement('div');
    dlg.className = 'search-wrap';
    dlg.hidden = true;
    dlg.innerHTML = `<div class="search-box" role="dialog" aria-modal="true" aria-label="${L.dlg}">
      <input type="search" class="search-input" placeholder="${L.ph}" autocomplete="off" aria-label="${L.what}">
      <ul class="search-list" role="listbox"></ul>
      <p class="search-hint">${L.hint}</p></div>`;
    document.body.appendChild(dlg);
    input = dlg.querySelector('.search-input');
    list = dlg.querySelector('.search-list');
    dlg.addEventListener('click', e => { if (e.target === dlg) close(); });
    input.addEventListener('input', run);
    input.addEventListener('keydown', e => {
      if (e.key === 'ArrowDown') { sel = Math.min(sel + 1, hits.length - 1); paint(); e.preventDefault(); }
      else if (e.key === 'ArrowUp') { sel = Math.max(sel - 1, 0); paint(); e.preventDefault(); }
      else if (e.key === 'Enter' && hits[sel]) { location.href = root + hits[sel].u; }
      else if (e.key === 'Escape') close();
    });
  }

  function snippet(text, q) {
    const i = norm(text).indexOf(q);
    if (i < 0) return esc(text.slice(0, 140)) + '…';
    const a = Math.max(0, i - 60), part = text.slice(a, i + q.length + 80);
    const j = i - a;
    return (a ? '…' : '') + esc(part.slice(0, j)) + '<mark>' + esc(part.slice(j, j + q.length)) + '</mark>' + esc(part.slice(j + q.length)) + '…';
  }

  function run() {
    const q = norm(input.value.trim());
    sel = 0;
    if (!q || !index) { hits = []; list.innerHTML = q ? '<li class="search-empty">' + L.load + '</li>' : ''; return; }
    const words = q.split(/\s+/);
    hits = index.map(it => {
      const t = norm(it.t), x = norm(it.x);
      if (!words.every(w => t.includes(w) || x.includes(w))) return null;
      const score = words.reduce((s, w) => s + (t.includes(w) ? 10 : 0) + (x.split(w).length - 1), 0);
      return { ...it, score };
    }).filter(Boolean).sort((a, b) => b.score - a.score).slice(0, 12);
    if (!hits.length) { list.innerHTML = '<li class="search-empty">' + L.none + '</li>'; return; }
    list.innerHTML = hits.map((h, i) => `<li role="option"><a href="${root + h.u}" data-i="${i}">
      <span class="search-kind">${esc(h.k)}</span><span class="search-title">${esc(h.t)}</span>
      <span class="search-snip">${snippet(h.x, words[0])}</span></a></li>`).join('');
    list.querySelectorAll('a').forEach(a => a.addEventListener('mousemove', () => { sel = +a.dataset.i; paint(); }));
    paint();
  }

  function paint() {
    list.querySelectorAll('li[role=option]').forEach((li, i) => li.classList.toggle('on', i === sel));
    const on = list.querySelector('li.on');
    if (on) on.scrollIntoView({ block: 'nearest' });
  }

  function open() {
    if (!dlg) build();
    dlg.hidden = false;
    document.body.classList.add('no-scroll');
    input.value = ''; list.innerHTML = ''; input.focus();
    if (!index) fetch(root + 'search.json').then(r => r.json()).then(d => { index = d; run(); })
      .catch(() => { list.innerHTML = '<li class="search-empty">' + L.off + '</li>'; });
  }
  function close() { dlg.hidden = true; document.body.classList.remove('no-scroll'); if (openBtn) openBtn.focus(); }

  if (openBtn) openBtn.addEventListener('click', open);
  document.addEventListener('keydown', e => {
    const typing = /INPUT|TEXTAREA/.test(document.activeElement.tagName);
    if ((e.key === '/' && !typing) || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k')) { e.preventDefault(); open(); }
  });
})();

/* Счётчики: «докручиваются» от нуля, когда попадают в экран */
(() => {
  const els = document.querySelectorAll('[data-count]');
  if (!els.length || matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;
  const run = el => {
    const end = +el.dataset.count, pre = el.dataset.prefix || '', suf = el.dataset.suffix || '', t0 = performance.now(), dur = 1400;
    const step = t => { const k = Math.min(1, (t - t0) / dur), v = Math.round(end * (1 - Math.pow(1 - k, 3)));
      el.textContent = pre + v + suf; if (k < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { run(e.target); io.unobserve(e.target); } }), { threshold: .4 });
  els.forEach(el => { el.textContent = (el.dataset.prefix || '') + '0' + (el.dataset.suffix || ''); io.observe(el); });
})();

/* Предпросмотр PDF в боковой панели: клик по ссылке на .pdf открывает файл справа, не уходя со страницы.
   Страницы рисует pdf.js (лежит в assets/vendor/pdfjs, грузится только при первом открытии) — одинаково во всех браузерах,
   включая телефоны. Если pdf.js не загрузился — встроенный просмотрщик браузера во фрейме. */
(() => {
  const EN = document.documentElement.lang === 'en';
  const L = EN ? { title: 'Preview', open: 'Open in new tab', dl: 'Download', close: 'Close preview', load: 'Loading…', page: 'pages' }
               : { title: 'Предпросмотр', open: 'Открыть в новой вкладке', dl: 'Скачать', close: 'Закрыть предпросмотр', load: 'Загружаю…', page: 'стр.' };
  const me = document.querySelector('script[src*="assets/site.js"]');
  const vendor = me ? new URL('vendor/pdfjs/', me.src).href : 'assets/vendor/pdfjs/';
  let panel, pages, nameEl, openA, dlA, countEl, lastFocus, libP, doc, io, token = 0;
  const loadLib = () => libP || (libP = new Promise((ok, fail) => {
    if (window.pdfjsLib) return ok(window.pdfjsLib);
    const sc = document.createElement('script'); sc.src = vendor + 'pdf.min.js';
    sc.onload = () => { window.pdfjsLib.GlobalWorkerOptions.workerSrc = vendor + 'pdf.worker.min.js'; ok(window.pdfjsLib); };
    sc.onerror = fail; document.head.appendChild(sc);
  }));
  const build = () => {
    panel = document.createElement('div');
    panel.className = 'pdfp'; panel.hidden = true;
    panel.innerHTML = `<div class="pdfp-back" data-close></div>
      <aside class="pdfp-box" role="dialog" aria-modal="true" aria-label="${L.title}">
        <header class="pdfp-head"><span class="pdfp-name"></span><span class="pdfp-count"></span>
          <a class="pdfp-btn pdfp-open" target="_blank" rel="noopener">${L.open} ↗</a>
          <a class="pdfp-btn pdfp-dl" download>${L.dl}</a>
          <button type="button" class="pdfp-x" data-close aria-label="${L.close}">✕</button></header>
        <div class="pdfp-pages" tabindex="0"></div></aside>`;
    document.body.appendChild(panel);
    pages = panel.querySelector('.pdfp-pages'); nameEl = panel.querySelector('.pdfp-name'); countEl = panel.querySelector('.pdfp-count');
    openA = panel.querySelector('.pdfp-open'); dlA = panel.querySelector('.pdfp-dl');
    panel.addEventListener('click', e => { if (e.target.closest('[data-close]')) close(); });
  };
  const render = async (href, my) => {
    pages.innerHTML = `<p class="pdfp-msg">${L.load}</p>`;
    try {
      const lib = await loadLib(); if (my !== token) return;
      doc = await lib.getDocument(href).promise; if (my !== token) return;
      countEl.textContent = doc.numPages + ' ' + L.page;
      const first = await doc.getPage(1), vp1 = first.getViewport({ scale: 1 });
      pages.innerHTML = '';
      const ph = [];
      for (let n = 1; n <= doc.numPages; n++) {
        const d = document.createElement('div'); d.className = 'pdfp-page'; d.dataset.n = n;
        d.style.aspectRatio = vp1.width + ' / ' + vp1.height; pages.appendChild(d); ph.push(d);
      }
      io = new IntersectionObserver(es => es.forEach(async e => {
        if (!e.isIntersecting || e.target.dataset.done) return;
        e.target.dataset.done = 1; io.unobserve(e.target);
        const pg = await doc.getPage(+e.target.dataset.n); if (my !== token) return;
        const w = e.target.clientWidth, base = pg.getViewport({ scale: 1 }), dpr = Math.min(devicePixelRatio || 1, 2);
        const vp = pg.getViewport({ scale: w / base.width * dpr });
        const c = document.createElement('canvas'); c.width = vp.width; c.height = vp.height;
        e.target.style.aspectRatio = base.width + ' / ' + base.height; e.target.appendChild(c);
        pg.render({ canvasContext: c.getContext('2d'), viewport: vp });
      }), { root: pages, rootMargin: '600px 0px' });
      ph.forEach(d => io.observe(d));
    } catch (err) {
      if (my !== token) return;
      pages.innerHTML = `<iframe class="pdfp-frame" title="${L.title}" src="${href}#view=FitH"></iframe>`;
    }
  };
  const open = (href, label) => {
    if (!panel) build();
    lastFocus = document.activeElement; token++;
    nameEl.textContent = label || decodeURIComponent(href.split('/').pop());
    countEl.textContent = ''; openA.href = href; dlA.href = href;
    panel.hidden = false; document.body.classList.add('no-scroll');
    requestAnimationFrame(() => panel.classList.add('on'));
    panel.querySelector('.pdfp-x').focus();
    render(href, token);
  };
  const close = () => {
    if (!panel || panel.hidden) return;
    token++; if (io) io.disconnect(); if (doc) { doc.destroy(); doc = null; }
    panel.classList.remove('on'); document.body.classList.remove('no-scroll');
    setTimeout(() => { panel.hidden = true; pages.innerHTML = ''; }, 200);
    if (lastFocus) lastFocus.focus();
  };
  const labelFor = a => {
    const t = (a.textContent || '').replace(/[↗→]/g, '').trim();
    const box = a.closest('li, article, section, .uni, .pj');
    const h = box && box.querySelector('h1, h2, h3, .pj-title, .what');
    const ht = h ? (h.childNodes[0] && h.childNodes[0].textContent || h.textContent).trim() : '';
    return ht && !t.toLowerCase().includes(ht.toLowerCase()) ? ht + ' — ' + t : (t || ht);
  };
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href]');
    if (!a || a.closest('.pdfp') || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
    if (!/\.pdf(#.*)?$/i.test(a.getAttribute('href'))) return;
    e.preventDefault();
    open(a.href.replace(/#.*$/, ''), labelFor(a));
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
})();
