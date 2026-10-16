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
  const norm = s => s.toLowerCase().replace(/ё/g, 'е');

  function build() {
    dlg = document.createElement('div');
    dlg.className = 'search-wrap';
    dlg.hidden = true;
    dlg.innerHTML = `<div class="search-box" role="dialog" aria-modal="true" aria-label="Поиск по сайту">
      <input type="search" class="search-input" placeholder="Поиск: посты, кейсы, проекты…" autocomplete="off" aria-label="Что ищем">
      <ul class="search-list" role="listbox"></ul>
      <p class="search-hint">↑↓ навигация · ↵ открыть · esc закрыть</p></div>`;
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
    if (!q || !index) { hits = []; list.innerHTML = q ? '<li class="search-empty">Загружаю…</li>' : ''; return; }
    const words = q.split(/\s+/);
    hits = index.map(it => {
      const t = norm(it.t), x = norm(it.x);
      if (!words.every(w => t.includes(w) || x.includes(w))) return null;
      const score = words.reduce((s, w) => s + (t.includes(w) ? 10 : 0) + (x.split(w).length - 1), 0);
      return { ...it, score };
    }).filter(Boolean).sort((a, b) => b.score - a.score).slice(0, 12);
    if (!hits.length) { list.innerHTML = '<li class="search-empty">Ничего не нашлось</li>'; return; }
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
      .catch(() => { list.innerHTML = '<li class="search-empty">Поиск недоступен</li>'; });
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
