const EN = document.documentElement.lang === 'en';
/* Солнечная диаграмма тем: внутреннее кольцо — группы, внешнее — теги; размер — сколько раз тег встречался до выбранного года. */
(() => {
  const D = window.EVO, svg = document.getElementById('sun');
  if (!D || !svg) return;
  const NS = 'http://www.w3.org/2000/svg', R0 = 62, R1 = 150, R2 = 250;
  const slider = document.getElementById('evo-year'), play = document.getElementById('evo-play'), sum = document.getElementById('evo-sum');
  const el = (n, a) => { const e = document.createElementNS(NS, n); for (const k in a) e.setAttribute(k, a[k]); return e; };
  const pt = (r, a) => [r * Math.sin(a), -r * Math.cos(a)];
  function arc(r1, r2, a1, a2) {
    if (a2 - a1 >= Math.PI * 2 - 1e-6) a2 = a1 + Math.PI * 2 - 1e-4;
    const big = a2 - a1 > Math.PI ? 1 : 0, [x1, y1] = pt(r2, a1), [x2, y2] = pt(r2, a2), [x3, y3] = pt(r1, a2), [x4, y4] = pt(r1, a1);
    return `M${x1},${y1}A${r2},${r2} 0 ${big} 1 ${x2},${y2}L${x3},${y3}A${r1},${r1} 0 ${big} 0 ${x4},${y4}Z`;
  }
  function shade(hex, k) {  // осветление цвета: k от 0 до 1
    const n = parseInt(hex.slice(1), 16), c = [n >> 16, (n >> 8) & 255, n & 255].map(v => Math.round(v + (255 - v) * k));
    return `rgb(${c.join(',')})`;
  }
  const plural = (n, a, b, c) => n % 10 === 1 && n % 100 !== 11 ? a : (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14) ? b : c);
  function draw(year) {
    const items = D.items.filter(i => i.y <= year), cnt = {};
    items.forEach(i => i.t.forEach(t => cnt[t] = (cnt[t] || 0) + 1));
    const groups = D.groups.map(g => {
      const tags = g.tags.filter(t => cnt[t]).sort((a, b) => cnt[b] - cnt[a]).map(t => ({ t, n: cnt[t] }));
      return { ...g, tags, n: tags.reduce((s, x) => s + x.n, 0) };
    }).filter(g => g.n);
    const total = groups.reduce((s, g) => s + g.n, 0);
    svg.innerHTML = '';
    let a = 0;
    groups.forEach(g => {
      const ga = g.n / total * Math.PI * 2, gEnd = a + ga;
      const gp = el('path', { d: arc(R0, R1, a, gEnd), fill: shade(g.color, .35), class: 'sb-g' });
      gp.appendChild(el('title', {})).textContent = `${g.name}: ${g.n}`;
      svg.appendChild(gp);
      if (ga > .35) {  // подпись группы по дуге
        const id = 'gp' + Math.round(a * 1000), mid = a + ga / 2, flip = mid > Math.PI / 2 && mid < Math.PI * 1.5, r = (R0 + R1) / 2 + (flip ? 5 : -5);
        const [sx, sy] = pt(r, flip ? gEnd - .04 : a + .04), [ex, ey] = pt(r, flip ? a + .04 : gEnd - .04);
        svg.appendChild(el('path', { id, d: `M${sx},${sy}A${r},${r} 0 ${ga > Math.PI ? 1 : 0} ${flip ? 0 : 1} ${ex},${ey}`, fill: 'none' }));
        const tx = el('text', { class: 'sb-gl' }), tp = el('textPath', { href: '#' + id, startOffset: '50%', 'text-anchor': 'middle' });
        tp.textContent = g.name.toUpperCase(); tx.appendChild(tp); svg.appendChild(tx);
      }
      let b = a;
      g.tags.forEach((x, i) => {
        const ta = x.n / total * Math.PI * 2, link = el('a', { href: D.links[x.t] || '#' });
        const p = el('path', { d: arc(R1 + 2, R2, b, b + ta), fill: shade(g.color, .08 + .5 * i / Math.max(g.tags.length, 4)), class: 'sb-t' });
        p.appendChild(el('title', {})).textContent = `${x.t}: ${x.n}`;
        link.appendChild(p); svg.appendChild(link);
        if (ta > .06) {
          const mid = b + ta / 2, [lx, ly] = pt(R2 + 12, mid), anchor = Math.sin(mid) > .1 ? 'start' : Math.sin(mid) < -.1 ? 'end' : 'middle';
          const lab = el('text', { x: lx, y: ly + 4, 'text-anchor': anchor, class: 'sb-tl' }); lab.textContent = x.t; svg.appendChild(lab);
        }
        b += ta;
      });
      a = gEnd;
    });
    svg.appendChild(el('circle', { r: R0 - 4, class: 'sb-c' }));
    const n1 = el('text', { y: 4, 'text-anchor': 'middle', class: 'sb-n' }); n1.textContent = items.length; svg.appendChild(n1);
    const n2 = el('text', { y: 28, 'text-anchor': 'middle', class: 'sb-s' }); n2.textContent = EN ? `items · ${year}` : `материалов · ${year}`; svg.appendChild(n2);
    const tagsN = Object.keys(cnt).length;
    sum.innerHTML = EN ? `<b>${tagsN}</b> ${tagsN === 1 ? 'tag' : 'tags'} · <b>${items.length}</b> ${items.length === 1 ? 'item' : 'items'} · <b>${year}</b>` : `<b>${tagsN}</b> ${plural(tagsN, 'тег', 'тега', 'тегов')} · <b>${items.length}</b> ${plural(items.length, 'материал', 'материала', 'материалов')} · <b>${year}</b> г.`;
  }
  slider.addEventListener('input', () => draw(+slider.value));
  let timer = null;
  play.addEventListener('click', () => {
    if (timer) { clearInterval(timer); timer = null; play.textContent = '▶'; return; }
    if (+slider.value >= +slider.max) slider.value = slider.min;
    play.textContent = '❚❚'; draw(+slider.value);
    timer = setInterval(() => {
      if (+slider.value >= +slider.max) { clearInterval(timer); timer = null; play.textContent = '▶'; return; }
      slider.value = +slider.value + 1; draw(+slider.value);
    }, 900);
  });
  draw(+slider.value);
})();
