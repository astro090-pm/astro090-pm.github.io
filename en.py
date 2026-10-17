"""Английская версия всего сайта (/en/).

Берёт те же функции сборки из build.py, подменяет данные и шапку на английские,
читает переведённые посты и кейсы из i18n_en/content, переводит оставшиеся
строки интерфейса и проверяет, что на страницах не осталось кириллицы.
"""
import json
import posixpath
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "i18n_en"
OUT = ROOT / "en"
CYR = re.compile(r"[А-Яа-яЁё][А-Яа-яЁё\s«»—–\-,.:;!?()0-9%№]*")


def build(ctx):
    import build as B
    import en_data as D

    ru = {k: getattr(B, k) for k in ("TIMELINE", "MONTHS_NOM")}
    B.ROOT = SRC
    for k, v in D.PATCH.items():
        setattr(B, k, v)
    B._titles.clear()
    B.tag_slug = lambda t: re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

    def heat_block():
        B.TIMELINE, B.MONTHS_NOM = ru["TIMELINE"], ru["MONTHS_NOM"]
        try:
            return orig_heat()
        finally:
            B.TIMELINE, B.MONTHS_NOM = D.PATCH["TIMELINE"], D.PATCH["MONTHS_NOM"]
    orig_heat = B.heat_block
    B.heat_block = heat_block
    B.year_stats = D.year_stats(B)
    B.layout = D.layout(ctx)
    import en_pages
    en_pages.install(B)

    pages = {}
    posts = B.load_posts()
    n_pages = max(1, -(-len(posts) // B.PER_PAGE))
    for n in range(1, n_pages + 1):
        pages["index.html" if n == 1 else f"page{n}.html"] = B.index_page(posts, n)
    pages["cv.html"] = B.cv_page()
    pages["projects.html"] = B.projects_page()
    pages["research.html"] = B.research_page(posts)
    pages["study.html"] = B.study_page()
    pages["about.html"] = B.about_page()
    pages["timeline.html"] = B.timeline_page()
    pages["tools.html"] = B.toolkit_page()
    pages["now.html"] = B.now_page(posts)
    pages["skills.html"] = B.skills_page()
    pages["conferences.html"] = B.conferences_page()
    pages["agents.html"] = B.agents_page(posts)
    media = B.load_media()
    if any(media.values()):
        pages["media.html"] = B.media_page(media)
    books = B.load_books()
    if books:
        pages["books.html"] = B.books_page(books, posts)
    for name, h in B.tags_pages(posts).items():
        pages[f"tags/{name}"] = h
    pages["blog/index.html"] = B.blog_index_page(posts)
    for p in posts:
        pages[f"blog/{p['slug']}.html"] = B.post_page(p, posts)
    pages["cases/index.html"] = B.cases_index_page()
    for i, c in enumerate(B.CASES):
        pages[f"cases/{c[0]}.html"] = B.case_page(i)

    import shutil
    if OUT.exists():
        shutil.rmtree(OUT)
    leftovers = {}
    for path, h in pages.items():
        h = D.translate(h)
        h = fix_assets(h, path)
        pages[path] = h
        for m in CYR.findall(re.sub(r"<(script|style)\b.*?</\1>", "", h, flags=re.S)):
            m = m.strip()
            if len(m) > 1:
                leftovers.setdefault(m, set()).add(path)
        f = OUT / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(h, encoding="utf-8")
    (OUT / "decks.html").write_text('<!doctype html><meta charset="utf-8"><title>Projects</title><meta http-equiv="refresh" content="0; url=projects.html"><link rel="canonical" href="projects.html"><a href="projects.html">Projects</a>', encoding="utf-8")
    search_index(pages)
    link_tag_pages(B, D)
    if leftovers:
        print(f"EN: осталась кириллица ({len(leftovers)}):")
        for k, v in sorted(leftovers.items(), key=lambda kv: -len(kv[1]))[:80]:
            print("  ", repr(k[:90]), "→", sorted(v)[:3])
    return len(pages)


def fix_assets(h, path):
    """Ссылки на assets/ и PDF ведут в корень сайта, а не в en/assets/."""
    base = posixpath.dirname("en/" + path)

    def fix(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r"^(https?:|mailto:|#|data:|/)", url):
            return m.group(0)
        target = posixpath.normpath(posixpath.join(base, url.split("#")[0].split("?")[0]))
        if target.startswith("en/assets/"):
            real = target[3:]
            rel = posixpath.relpath(real, base) + url[len(url.split("#")[0].split("?")[0]):]
            return f'{attr}="{rel}"'
        return m.group(0)
    return re.sub(r'(href|src)="([^"]+)"', fix, h)


def search_index(pages):
    items = []
    for path, h in pages.items():
        if path.startswith("tags/") or re.match(r"page\d+\.html$", path) or path in ("blog/index.html", "index.html"):
            continue
        t = re.search(r"<title>(.*?)</title>", h)
        title = (t.group(1) if t else path).replace(" — Roman Ponurov", "")
        main = re.search(r"<main>(.*)</main>", h, re.S)
        body = main.group(1) if main else ""
        body = re.sub(r"<(script|style|nav)\b.*?</\1>", " ", body, flags=re.S)
        body = re.sub(r'<section class="related-posts">.*?</section>|<div class="post-actions">.*?</div>|<a class="back"[^>]*>.*?</a>|<p class="post-meta">.*?</p>', " ", body, flags=re.S)
        import html as _h
        text = _h.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body))).strip()
        title = _h.unescape(title).replace(" — a case by Roman Ponurov", "")
        kind = {"blog": "post", "cases": "case"}.get(path.split("/")[0], "page") if "/" in path else "page"
        items.append({"t": title, "u": path, "k": kind, "x": text[:6000]})
    (OUT / "search.json").write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")


def link_tag_pages(B, D):
    """Переключатель языка на страницах тегов: у тега разные слаги в русской и английской версиях."""
    tr = dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
                  ["a","b","v","g","d","e","e","zh","z","i","y","k","l","m","n","o","p","r","s","t","u","f",
                   "h","ts","ch","sh","sch","","y","","e","yu","ya"]))
    ru = lambda t: re.sub(r"[^a-z0-9]+", "-", "".join(tr.get(c, c) for c in t.lower())).strip("-")
    en = B.tag_slug
    for r, e in D.TAG_RU_EN.items():
        rs, es = ru(r), en(e)
        if rs == es:
            continue
        f = ROOT / "tags" / f"{rs}.html"
        if f.exists():
            f.write_text(f.read_text(encoding="utf-8").replace(f'href="../en/tags/{rs}.html"', f'href="../en/tags/{es}.html"'), encoding="utf-8")
        g = OUT / "tags" / f"{es}.html"
        if g.exists():
            g.write_text(g.read_text(encoding="utf-8").replace(f'href="../../tags/{es}.html"', f'href="../../tags/{rs}.html"')
                         .replace(f'hreflang="ru" href="{"https://astro090-pm.github.io"}/tags/{es}.html"', f'hreflang="ru" href="https://astro090-pm.github.io/tags/{rs}.html"'), encoding="utf-8")
