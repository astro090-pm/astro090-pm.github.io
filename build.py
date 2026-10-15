"""Сборка сайта-портфолио: python build.py  →  главная с лентой постов, кейсы, резюме, проекты, теги.

Тексты кейсов лежат в content/cases/*.md (те же, что в репозитории product-cases).
Чтобы добавить кейс: положите .md в content/cases и добавьте строку в CASES ниже.
Нужен пакет markdown:  pip install markdown
"""

from __future__ import annotations

import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
SITE_URL = "https://astro090-pm.github.io"
GITHUB = "https://github.com/astro090-pm"

# Кейсы в порядке показа: (slug, компания, годы, тип, короткое описание, ключевой результат)
CASES = [
    ("asia-online", "Азия Ритейл", "2023–2024", "B2C, ~600 тыс. пользователей",
     "Перезапуск онлайн-доставки продуктов: приложение, оплата, сборка заказов, партнёрства с Glovo и банком.",
     "Выручка +103%, заказы +67%, отток −24%"),
    ("mts-id", "МТС", "2021–2023", "B2B2C, ~10 млн пользователей",
     "Единая бесшовная авторизация в продуктах экосистемы и переход с монолита на микросервисы.",
     "Подключены 9 флагманских продуктов и МТС Банк, бесшовные входы +23%"),
    ("po-sosedstvu", "По соседству", "2022–2024", "B2C и B2B, сооснователь",
     "Вывод офлайн-магазина в онлайн с внешней командой и небольшим бюджетом.",
     "B2B: заказы +89%, средний чек +71%, выручка +58%"),
    ("gazprombank", "Газпромбанк", "с 2024", "B2E, 1 000 сотрудников",
     "Внутренний сервис кредитного анализа компаний с ИИ-агентом: от концепции и защиты бюджета до запуска.",
     "Запущен с нуля в промышленную эксплуатацию"),
    ("dobster", "Добстер", "2022–2023", "B2C, сооснователь",
     "Платформа благотворительных услуг: концепция, мокапы, команда, запуск.",
     "Запущена с нуля до продакшена"),
    ("granit", "Концерн ГРАНИТ", "2019–2021", "B2G, 50 пользователей",
     "Автоматизация процессов государственного департамента; путь из системного аналитика в продакты.",
     "Сервис запущен с нуля"),
    ("bolz", "Собственный проект", "2025", "B2C",
     "Агрегатор шеринг-сервисов в акселераторе Московского инновационного кластера.",
     "Участник «Новатор Москвы 2025»"),
]

# Метки кейсов: (сферы, модели, обложка: крупная надпись, подпись, цвет)
TAGS = {
    "asia-online": (["фудтех", "e-com"], ["B2C"], ("+103%", "выручка", "#F0C24B")),
    "mts-id": (["телеком", "платформа"], ["B2B2C"], ("10 млн", "пользователей", "#BFD3F2")),
    "po-sosedstvu": (["фудтех", "e-com"], ["B2C", "B2B"], ("+89%", "заказов B2B", "#F0C24B")),
    "gazprombank": (["финтех", "AI"], ["B2E"], ("ИИ-агент", "в кредитном анализе", "#C9DDC5")),
    "dobster": (["благотворительность"], ["B2C"], ("0 → прод", "запуск с нуля", "#E8D3E0")),
    "granit": (["госсектор"], ["B2G"], ("B2G", "автоматизация процессов", "#D9DCD4")),
    "bolz": (["шеринг"], ["B2C"], ("2025", "акселератор МИК", "#BFD3F2")),
}

FONTS = ("https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600"
         "&family=Unbounded:wght@600;700&display=swap")


import hashlib
CSS_V = hashlib.md5((Path(__file__).parent / "assets" / "style.css").read_bytes()).hexdigest()[:8]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def layout(title: str, description: str, body: str, path: str, depth: int = 0) -> str:
    up = "../" * depth
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{SITE_URL}/{path}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{up}assets/style.css?v={CSS_V}">
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="{up}index.html"><img class="avatar avatar-sm" src="{up}assets/avatar-sm.jpg" width="34" height="34" alt="">Роман Понуров</a>
<nav class="nav" aria-label="Разделы">
<details class="menu"><summary>продакт</summary><div class="menu-list"><a href="{up}cv.html">📄 резюме</a><a href="{up}cases/index.html">📁 портфолио кейсов</a></div></details>
<details class="menu"><summary>наука</summary><div class="menu-list"><a href="{up}research.html">🎓 исследования</a><a href="{up}study.html">📚 учёба</a></div></details>
<a href="{up}projects.html">проекты</a>
<a href="{up}blog/index.html">посты</a>
<a href="{up}tags/index.html">теги</a>
</nav>
<script>
document.addEventListener('click', e => document.querySelectorAll('details.menu[open]').forEach(d => {{ if (!d.contains(e.target)) d.open = false; }}));
document.querySelectorAll('details.menu').forEach(d => d.addEventListener('toggle', () => {{ if (d.open) document.querySelectorAll('details.menu[open]').forEach(o => {{ if (o !== d) o.open = false; }}); }}));
</script>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap foot">
© 2026 Роман Понуров · <a href="mailto:ponurov.roman@yandex.ru">email</a> · <a href="https://t.me/astro090">telegram</a> · все права защищены
</div></footer>
</body>
</html>
"""


PER_PAGE = 10


def tag_slug(t: str) -> str:
    tr = dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
                  ["a","b","v","g","d","e","e","zh","z","i","y","k","l","m","n","o","p","r","s","t","u","f",
                   "h","ts","ch","sh","sch","","y","","e","yu","ya"]))
    out = "".join(tr.get(c, c) for c in t.lower())
    return re.sub(r"[^a-z0-9]+", "-", out).strip("-")


def all_items(posts: list[dict]) -> list[dict]:
    """Посты и кейсы с метками — для облака тегов, страниц тегов и случайного перехода."""
    items = [{"title": p["title"], "url": f"blog/{p['slug']}.html", "tags": p["tags"], "kind": "пост",
              "date_h": p["date_h"], "year": int(p["date"][:4])} for p in posts]
    for slug, company, years, *_ in CASES:
        sph, mod, _cover = TAGS[slug]
        items.append({"title": case_title(slug), "url": f"cases/{slug}.html", "tags": ["продакт"] + sph + mod,
                      "kind": "кейс", "date_h": f"{company}, {years}", "year": int(re.findall(r"\d{4}", years)[0])})
    return items


def tag_counts(items: list[dict]) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    for it in items:
        for t in it["tags"]:
            counts[t] = counts.get(t, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def tag_cloud(items: list[dict], prefix: str) -> str:
    return "".join(f'<a class="chip" href="{prefix}tags/{tag_slug(t)}.html">{esc(t)} <span>{n}</span></a>'
                   for t, n in tag_counts(items))


def feed(posts: list[dict], prefix: str) -> str:
    return "\n".join(
        f"""<li class="feed-item"><a class="feed-link" href="{prefix}{p['slug']}.html">
<time datetime="{p['date']}">{p['date_h']}</time>
<span class="feed-title">{esc(p['title'])}</span>
<span class="feed-excerpt">{esc(p['excerpt'])}</span></a></li>"""
        for p in posts)


def pager(page: int, pages: int) -> str:
    if pages <= 1:
        return ""
    href = lambda n: "index.html" if n == 1 else f"page{n}.html"
    newer = f'<a href="{href(page - 1)}">свежее</a>' if page > 1 else "<span></span>"
    older = f'<a href="{href(page + 1)}">старее</a>' if page < pages else "<span></span>"
    return f'<nav class="pager" aria-label="Страницы ленты">{newer}<span>страница {page} из {pages}</span>{older}</nav>'


def index_page(posts: list[dict], page: int = 1) -> str:
    items = all_items(posts)
    pages = max(1, -(-len(posts) // PER_PAGE))
    chunk = posts[(page - 1) * PER_PAGE: page * PER_PAGE]
    urls = ",".join(f'"{it["url"]}"' for it in items)
    body = f"""
<div class="wrap home">

<section class="hero-home">
<img class="avatar avatar-lg" src="assets/avatar.jpg" width="160" height="160" alt="Роман Понуров">
<div>
<h1>Роман Понуров</h1>
<p class="roles"><a href="cv.html">менеджер продукта</a>, <a href="tags/{tag_slug('преподавание')}.html">преподаватель</a> и <a href="research.html">исследователь ИИ в управлении</a></p>
<button type="button" class="random" id="random">случайный пост</button>
</div>
</section>

<section aria-label="Лента постов">
<ul class="feed">
{feed(chunk, "blog/")}
</ul>
{pager(page, pages)}
<p class="all-posts"><a href="blog/index.html">Все посты</a></p>
</section>
</div>
<script>
document.getElementById('random').addEventListener('click', () => {{
  const urls = [{urls}];
  location.href = urls[Math.floor(Math.random() * urls.length)];
}});
</script>
"""
    return layout("Роман Понуров — менеджер продукта",
                  "Роман Понуров: менеджер продукта, преподаватель, исследователь ИИ в управлении. Посты, кейсы, проекты.",
                  body, "" if page == 1 else f"page{page}.html")


def cv_page() -> str:
    body = """
<section class="hero"><div class="wrap">
<a class="back" href="index.html">На главную</a>
<h1>Резюме</h1>
<p class="lead">Менеджер продукта. Шесть лет запускаю продукты с нуля и вывожу бизнес из офлайна в онлайн.</p>
<p class="lead">Работал в фудтехе, телекоме, финтехе и благотворительности — в B2C, B2B, B2E и B2G. Сейчас строю AI-продукты и исследую ИИ в управлении компанией.</p>
<p class="cv-link"><a href="assets/Ponurov_Roman_CV.pdf">Скачать резюме, PDF</a></p>
<div class="ledger" aria-label="Результаты">
<div class="ledger-row"><span class="num">+103%</span><span class="ledger-what">выручки после перезапуска онлайн-доставки продуктов</span><span class="ledger-where"><a href="cases/asia-online.html">Азия Онлайн, 2023–2024</a></span></div>
<div class="ledger-row"><span class="num">10 млн</span><span class="ledger-what">пользователей входят в 9 продуктов МТС через одну авторизацию</span><span class="ledger-where"><a href="cases/mts-id.html">MTS ID, 2021–2023</a></span></div>
<div class="ledger-row"><span class="num">+89%</span><span class="ledger-what">заказов от бизнес-клиентов после выхода магазина в онлайн</span><span class="ledger-where"><a href="cases/po-sosedstvu.html">По соседству, 2022–2024</a></span></div>
<div class="ledger-row"><span class="num">4</span><span class="ledger-what">продукта запущены с нуля, два из них — как сооснователь</span><span class="ledger-where"><a href="cases/index.html">все кейсы</a></span></div>
</div>
</div></section>

<section class="block" id="path"><div class="wrap">
<h2>Путь</h2>
<p class="intro">Из инженерии — в системный анализ, оттуда — в продакт-менеджмент.</p>
<ol class="path">
<li><span class="yrs">2014–2019</span>Инженер, затем менеджер по развитию бизнеса</li>
<li><span class="yrs">2019–2021</span>Системный аналитик, затем менеджер продукта — Концерн ГРАНИТ</li>
<li><span class="yrs">2021–2023</span>Менеджер продукта MTS ID — МТС</li>
<li><span class="yrs">2023–2024</span>Руководитель электронной коммерции — Азия Ритейл</li>
<li class="now"><span class="yrs">с 2024</span>Старший менеджер продукта — Газпромбанк</li>
</ol>
<p class="intro" style="margin-top:24px">Образование — на странице <a href="research.html">исследований</a>.</p>
</div></section>

<section class="block" id="contacts"><div class="wrap">
<h2>Контакты</h2>
<p class="intro">Открыт к разговору о продуктовых и AI-ролях.</p>
<div class="contacts">
<a href="https://t.me/astro090">Telegram: @astro090</a>
<a href="mailto:ponurov.roman@yandex.ru">ponurov.roman@yandex.ru</a>
<a href="https://www.linkedin.com/in/roman-ponurov-bb3b81a6/">LinkedIn</a>
<a href="https://github.com/astro090-pm">GitHub</a>
</div>
</div></section>
"""
    return layout("Резюме — Роман Понуров", "Резюме Романа Понурова: результаты, путь, контакты.", body, "cv.html")


OWN = [
    ("po-sosedstvu", "«По соседству»", "Сооснователь и менеджер продукта · 2022–2024",
     "Вывел офлайн-магазин продуктов в онлайн: интернет-магазин с доставкой для частных и корпоративных клиентов. Концепция, процессы, команда внешних исполнителей, запуск на 1С-Битрикс.",
     "B2B: заказы +89%, средний чек +71%, выручка +58%", ("po-sosedstvu.ru", "https://po-sosedstvu.ru/")),
    ("dobster", "«Добстер»", "Сооснователь и менеджер продукта · 2022–2023",
     "Платформа благотворительных услуг. Концепция и роадмап, мокапы, сбор команды, разработка на Python и React.",
     "Запущен с нуля до продакшена", None),
    ("bolz", "bolz", "Автор продукта · 2025",
     "Агрегатор шеринг-сервисов. Упаковка идеи, проверка гипотез и питч перед экспертами.",
     "Акселератор «Академия инноваторов» МИК, конкурс «Новатор Москвы 2025»", None),
]


def own_cards() -> str:
    out = []
    for slug, name, role, about, result, site in OWN:
        big, small, color = TAGS[slug][2]
        ext = f' · <a href="{site[1]}">{site[0]}</a>' if site else ""
        out.append(f"""<li class="card">
<a class="cover" href="cases/{slug}.html" style="background:{color}" tabindex="-1" aria-hidden="true"><span class="cover-big">{esc(big)}</span><span class="cover-small">{esc(small)}</span></a>
<p class="card-meta"><span class="card-co">{esc(role)}</span></p>
<h3 class="card-title"><a href="cases/{slug}.html">{esc(name)}</a></h3>
<p class="card-about">{esc(about)}</p>
<p class="card-result">{esc(result)}</p>
<p class="card-about"><a href="cases/{slug}.html">Подробнее о кейсе</a>{ext}</p>
</li>""")
    return "\n".join(out)


def projects_page() -> str:
    body = f"""
<article class="page"><div class="wrap">
<a class="back" href="index.html">На главную</a>
<h1>Проекты</h1>
<p class="intro">То, что я запускал сам — как сооснователь или автор, — и прототипы, на которых проверяю гипотезы про AI-продукты.</p>

<h2>Собственные проекты</h2>
<ul class="cards own">
{own_cards()}
</ul>

<h2 class="own-ai">AI-прототипы</h2>
<p class="intro">Код открыт.</p>
<article class="project">
<div>
<h3>Планировщик выходных</h3>
<p>Telegram-бот, который за минуту собирает план выходных по часам: смотрит погоду, афишу и места, укладывается в бюджет и учитывает возраст детей.</p>
<ul>
<li>Три агента: планировщик, разведчик и критик общаются по протоколу A2A</li>
<li>Инструменты вынесены в собственный MCP-сервер, есть браузерный агент</li>
<li>Модель только выбирает варианты — названия, цены и время подставляет код</li>
<li>32 эвал-кейса и продуктовые метрики: activation, возвраты, оценки</li>
</ul>
<p><a href="{GITHUB}/weekend-planner">Код и описание на GitHub</a></p>
</div>
<figure>
<img src="assets/weekend-planner-arch.png" width="1344" height="960" alt="Схема: пользователь пишет в Telegram-бот, тот передаёт запрос планировщику; планировщик по A2A обращается к разведчику и критику; разведчик через MCP-сервер получает погоду, афишу, места и читает страницы браузером.">
<figcaption>Кто с кем работает внутри бота</figcaption>
</figure>
</article>
</div></article>
"""
    return layout("Проекты — Роман Понуров", "AI-проекты Романа Понурова с открытым кодом.", body, "projects.html")


TAG_GROUPS = [
    ("продуктовое", ["продакт", "AI", "платформа", "e-com", "менеджмент"]),
    ("сферы", ["фудтех", "телеком", "финтех", "благотворительность", "госсектор", "шеринг"]),
    ("бизнес-модели", ["B2C", "B2B", "B2B2C", "B2E", "B2G"]),
    ("преподавание и наука", ["преподавание", "исследования"]),
]


def tags_pages(posts: list[dict]) -> dict[str, str]:
    items = all_items(posts)
    counts = dict(tag_counts(items))
    pages = {}
    link = lambda t: f'<a class="tag-link" href="{tag_slug(t)}.html">#{esc(t)}<sup>{counts[t]}</sup></a>'
    groups, used = [], set()
    for name, tags in TAG_GROUPS:
        present = sorted((t for t in tags if t in counts), key=lambda t: (-counts[t], t))
        used.update(present)
        if present:
            groups.append(f'<section class="tag-group"><h2>{esc(name)}</h2><p>{" ".join(link(t) for t in present)}</p></section>')
    rest = sorted((t for t in counts if t not in used), key=lambda t: (-counts[t], t))
    if rest:
        groups.append(f'<section class="tag-group"><h2>без категории</h2><p>{" ".join(link(t) for t in rest)}</p></section>')
    # как развивались темы: по годам — какие метки появлялись в постах и кейсах
    years = sorted({it["year"] for it in items})
    rows = []
    for y in years:
        yc: dict[str, int] = {}
        for it in items:
            if it["year"] == y:
                for t in it["tags"]:
                    yc[t] = yc.get(t, 0) + 1
        top = sorted(yc.items(), key=lambda kv: (-kv[1], kv[0]))
        rows.append(f'<li><span class="yrs">{y}</span><span>{" ".join(link(t) for t, _ in top)}</span></li>')
    body = f"""
<article class="page"><div class="wrap">
<a class="back" href="../index.html">На главную</a>
<h1>Теги</h1>
{"".join(groups)}
<section class="tag-group"><h2>как развивались темы</h2>
<ol class="tag-years">{"".join(rows)}</ol>
</section>
</div></article>
"""
    pages["index.html"] = layout("Теги — Роман Понуров", "Все темы: посты и кейсы по меткам.", body, "tags/", depth=1)
    for t, n in tag_counts(items):
        rows = "\n".join(
            f'<li class="feed-item"><a class="feed-link" href="../{it["url"]}"><time>{esc(it["kind"])} · {esc(it["date_h"])}</time>'
            f'<span class="feed-title">{esc(it["title"])}</span></a></li>'
            for it in items if t in it["tags"])
        body = f"""
<article class="page"><div class="wrap">
<a class="back" href="index.html">Все теги</a>
<h1>{esc(t)}</h1>
<p class="intro">{n} материал(ов) с этой меткой.</p>
<ul class="feed">
{rows}
</ul>
</div></article>
"""
        pages[f"{tag_slug(t)}.html"] = layout(f"{t} — Роман Понуров", f"Посты и кейсы с меткой «{t}».", body,
                                              f"tags/{tag_slug(t)}.html", depth=1)
    return pages


_titles: dict[str, str] = {}


def case_title(slug: str) -> str:
    if slug not in _titles:
        text = (ROOT / "content" / "cases" / f"{slug}.md").read_text(encoding="utf-8")
        m = re.search(r"^#\s+(.+)$", text, re.M)
        _titles[slug] = m.group(1).strip() if m else slug
    return _titles[slug]


def case_page(i: int) -> str:
    slug, company, years, kind, about, _result = CASES[i]
    text = (ROOT / "content" / "cases" / f"{slug}.md").read_text(encoding="utf-8")
    text = re.sub(r"^#\s+.+\n", "", text, count=1)
    # GitHub допускает список сразу после строки текста, python-markdown — только после пустой строки.
    text = re.sub(r"(?m)^(?!- |\d+\. )(.+)\n(?=- |\d+\. )", r"\1\n\n", text)
    body_html = markdown.markdown(text, extensions=["tables", "sane_lists"])
    nxt = CASES[(i + 1) % len(CASES)]
    body = f"""
<article class="page"><div class="wrap">
<a class="back" href="index.html">Все кейсы</a>
<h1>{esc(case_title(slug))}</h1>
<div class="prose">
{body_html}
<p class="next-case">Следующий кейс: <a href="{nxt[0]}.html">{esc(case_title(nxt[0]))}</a></p>
</div>
</div></article>
"""
    return layout(f"{case_title(slug)} — кейс Романа Понурова", about, body, f"cases/{slug}.html", depth=1)


MONTHS_GEN = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября",
              "ноября", "декабря"]


def load_posts() -> list[dict]:
    """Посты: content/posts/ГГГГ-ММ-ДД-slug.md с шапкой title/date/tags. Новые — сверху."""
    posts = []
    for f in sorted((ROOT / "content" / "posts").glob("*.md")):
        raw = f.read_text(encoding="utf-8")
        meta, body = {}, raw
        m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
        if m:
            for line in m.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            body = raw[m.end():]
        y, mo, d = (int(x) for x in meta["date"].split("-"))
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body.strip().split("\n\n")[0])
        posts.append({
            "slug": f.stem[11:] if re.match(r"\d{4}-\d{2}-\d{2}-", f.stem) else f.stem,
            "title": meta["title"], "date": meta["date"], "date_h": f"{d} {MONTHS_GEN[mo - 1]} {y}",
            "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
            "excerpt": text, "body": body,
        })
    return sorted(posts, key=lambda p: p["date"], reverse=True)


def post_list(posts: list[dict], prefix: str) -> str:
    return "\n".join(
        f"""<li class="post-item"><time datetime="{p['date']}">{p['date_h']}</time>
<div><h3><a href="{prefix}{p['slug']}.html">{esc(p['title'])}</a></h3>
<p>{esc(p['excerpt'])}</p></div></li>"""
        for p in posts)


def post_page(p: dict) -> str:
    body_html = markdown.markdown(p["body"], extensions=["tables", "sane_lists"])
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in p["tags"])
    body = f"""
<article class="page"><div class="wrap">
<a class="back" href="index.html">Все посты</a>
<h1>{esc(p['title'])}</h1>
<p class="post-meta"><time datetime="{p['date']}">{p['date_h']}</time>{tags}</p>
<div class="prose">
{body_html}
</div>
</div></article>
"""
    return layout(f"{p['title']} — Роман Понуров", p["excerpt"][:160], body, f"blog/{p['slug']}.html", depth=1)


def blog_index_page(posts: list[dict]) -> str:
    body = f"""
<article class="page"><div class="wrap">
<a class="back" href="../index.html">На главную</a>
<h1>Посты</h1>
<p class="intro">Короткие заметки о работе, продуктах и преподавании.</p>
<ul class="posts">
{post_list(posts, "")}
</ul>
</div></article>
"""
    return layout("Посты — Роман Понуров", "Заметки Романа Понурова о продуктах, AI и преподавании.", body, "blog/", depth=1)


def cases_index_page() -> str:
    spheres = sorted({t for v in TAGS.values() for t in v[0]})
    models = sorted({t for v in TAGS.values() for t in v[1]})
    chips = "".join(f'<button type="button" class="chip" data-tag="{esc(t)}" aria-pressed="false">{esc(t)}</button>'
                    for t in spheres + models)
    cards = []
    for slug, company, years, _kind, about, result in CASES:
        sph, mod, (big, small, color) = TAGS[slug]
        tags = " ".join(sph + mod)
        meta = "".join(f'<span class="tag">{esc(t)}</span>' for t in sph + mod)
        cards.append(f"""<li class="card" data-tags="{esc(tags)}">
<a class="cover" href="{slug}.html" style="background:{color}" aria-hidden="true" tabindex="-1">
<span class="cover-big">{esc(big)}</span><span class="cover-small">{esc(small)}</span></a>
<p class="card-meta"><span class="card-co">{esc(company)}, {esc(years)}</span>{meta}</p>
<h2 class="card-title"><a href="{slug}.html">{esc(case_title(slug))}</a></h2>
<p class="card-about">{esc(about)}</p>
<p class="card-result">{esc(result)}</p>
</li>""")
    body = f"""
<article class="page"><div class="wrap">
<a class="back" href="../index.html">На главную</a>
<h1>Портфолио кейсов</h1>
<p class="intro">Продукты, которые я запускал и развивал за шесть лет: от онлайн-доставки продуктов до авторизации на 10 млн пользователей. По каждому кейсу — контекст, что я сделал и к чему это привело.</p>
<div class="filters" role="group" aria-label="Фильтр по меткам">
<button type="button" class="chip" data-tag="" aria-pressed="true">все {len(CASES)}</button>{chips}
</div>
<p class="filter-empty" hidden>Под эту метку кейсов нет — выберите другую.</p>
<ul class="cards">
{chr(10).join(cards)}
</ul>
<nav class="related" aria-label="Другие разделы">
<h2>Ещё на сайте</h2>
<ul>
<li><a href="../projects.html">Проекты</a> — AI-прототипы с открытым кодом</li>
<li><a href="../research.html">Исследования и образование</a> — ИИ в управлении компанией</li>
<li><a href="../assets/Ponurov_Roman_CV.pdf">Резюме, PDF</a></li>
</ul>
</nav>
</div></article>
<script>
(() => {{
  const chips = document.querySelectorAll('.chip');
  const cards = document.querySelectorAll('.card');
  const empty = document.querySelector('.filter-empty');
  chips.forEach(chip => chip.addEventListener('click', () => {{
    const tag = chip.dataset.tag;
    chips.forEach(c => c.setAttribute('aria-pressed', String(c === chip)));
    let shown = 0;
    cards.forEach(card => {{
      const on = !tag || card.dataset.tags.split(' ').includes(tag);
      card.hidden = !on; if (on) shown++;
    }});
    empty.hidden = shown > 0;
  }}));
}})();
</script>
"""
    return layout("Портфолио кейсов — Роман Понуров",
                  "Продуктовые кейсы Романа Понурова: e-commerce, телеком, финтех, B2G и собственные проекты.",
                  body, "cases/", depth=1)


def research_page() -> str:
    body = """
<article class="page"><div class="wrap">
<a class="back" href="index.html">На главную</a>
<h1>Исследования и образование</h1>

<section class="uni">
<div class="uni-head"><h2><img class="uni-logo" src="assets/uni/ranepa.png" width="35" height="64" alt="">РАНХиГС</h2><p class="uni-meta">Аспирантура, менеджмент<br>Москва, 2024–2027</p></div>
<p class="uni-topic">Диссертация: «Использование искусственного интеллекта для совершенствования системы управления компанией».</p>
<ul class="pubs">
<li><span class="when">Март 2026<br>доклад</span><span class="what">Технологические требования к инфраструктуре компании при внедрении искусственного интеллекта<i>CIV Международная научно-практическая конференция «Актуальные вопросы экономических наук и современного менеджмента»</i></span></li>
<li><span class="when">Декабрь 2025<br>ВАК, К2</span><span class="what">Риски и ограничения применения искусственного интеллекта в управлении компанией<i>Экономика и управление: проблемы, решения</i></span></li>
<li><span class="when">Сентябрь 2025<br>ВАК, К2</span><span class="what">Современные тенденции использования искусственного интеллекта в корпоративном управлении в период цифровой трансформации<i>Финансовый менеджмент</i></span></li>
<li><span class="when">Май 2025<br>ВАК, К2</span><span class="what">Характерные особенности применения искусственного интеллекта в менеджменте российских компаний<i>Экономика и управление: проблемы, решения</i></span></li>
</ul>
</section>

<section class="uni">
<div class="uni-head"><h2><img class="uni-logo" src="assets/uni/hse.png" width="64" height="64" alt="">НИУ ВШЭ</h2><p class="uni-meta">Магистратура, корпоративные финансы<br>Москва, 2018–2021</p></div>
<p class="uni-topic">Выпускная работа: «Моделирование и оценка эффективности инвестиционных проектов в области цифровой трансформации компании».</p>
</section>

<section class="uni">
<div class="uni-head"><h2><img class="uni-logo" src="assets/uni/mei.png" width="136" height="64" alt="">НИУ МЭИ</h2><p class="uni-meta">Электротехника<br>Москва, 2008–2015</p></div>
<p class="uni-topic">Инженерная база, с которой начался путь: испытания и обслуживание электрооборудования, затем продажи технических решений.</p>
</section>
</div></article>
"""
    return layout("Исследования и образование — Роман Понуров",
                  "Исследования об использовании искусственного интеллекта в управлении компанией и образование.",
                  body, "research.html")


STUDY = [
    ("Сертификаты", [
        ("Scrum.org", "Professional Scrum Product Owner I (PSPO I)", "Сертификат владельца продукта по Scrum: ценность продукта, бэклог, работа со стейкхолдерами.", "сертификат"),
        ("Cambridge English", "Business English Certificate (BEC)", "Деловой английский, уровень B1.", "сертификат"),
    ]),
    ("Курсы", [
        ("Pendo.io · 2023", "AI for Product Management", "Как применять ИИ в работе продакт-менеджера и в самих продуктах.", "курс"),
        ("GoPractice · 2022", "Симулятор управления продуктом", "Продуктовая аналитика и метрики на сквозном кейсе: от гипотезы до решения по данным.", "курс"),
    ]),
    ("Акселераторы", [
        ("Московский инновационный кластер · 2025", "«Академия инноваторов»", "Акселератор с проектом bolz: упаковка идеи, проверка гипотез, питч перед экспертами. Затем — конкурс «Новатор Москвы 2025».", "акселератор"),
    ]),
]


def study_page() -> str:
    blocks = []
    for title, rows in STUDY:
        lis = "\n".join(
            f'<li><span class="when">{esc(org)}<br>{esc(kind)}</span><span class="what">{esc(name)}<i>{esc(about)}</i></span></li>'
            for org, name, about, kind in rows)
        blocks.append(f'<section class="uni"><div class="uni-head"><h2>{esc(title)}</h2></div><ul class="pubs">\n{lis}\n</ul></section>')
    body = f"""
<article class="page"><div class="wrap">
<a class="back" href="index.html">На главную</a>
<h1>Учёба</h1>
<p class="intro">Сертификаты, курсы и программы, которые я прошёл помимо университетов. Высшее образование и аспирантура — на странице <a href="research.html">исследований</a>.</p>
{"".join(blocks)}
</div></article>
"""
    return layout("Учёба — Роман Понуров", "Сертификаты, курсы и акселераторы Романа Понурова.", body, "study.html")


def main() -> None:
    posts = load_posts()
    pages = max(1, -(-len(posts) // PER_PAGE))
    for n in range(1, pages + 1):
        (ROOT / ("index.html" if n == 1 else f"page{n}.html")).write_text(index_page(posts, n), encoding="utf-8")
    (ROOT / "cv.html").write_text(cv_page(), encoding="utf-8")
    (ROOT / "projects.html").write_text(projects_page(), encoding="utf-8")
    (ROOT / "research.html").write_text(research_page(), encoding="utf-8")
    (ROOT / "study.html").write_text(study_page(), encoding="utf-8")
    for d in ("blog", "cases", "tags"):
        (ROOT / d).mkdir(exist_ok=True)
    for f in (ROOT / "tags").glob("*.html"):
        f.unlink()
    for name, html_ in tags_pages(posts).items():
        (ROOT / "tags" / name).write_text(html_, encoding="utf-8")
    (ROOT / "blog" / "index.html").write_text(blog_index_page(posts), encoding="utf-8")
    for p in posts:
        (ROOT / "blog" / f"{p['slug']}.html").write_text(post_page(p), encoding="utf-8")
    (ROOT / "cases" / "index.html").write_text(cases_index_page(), encoding="utf-8")
    for i, case in enumerate(CASES):
        (ROOT / "cases" / f"{case[0]}.html").write_text(case_page(i), encoding="utf-8")
    print(f"Готово: главная, {len(posts)} пост(ов), {len(CASES)} кейсов, резюме, проекты, исследования, теги")


if __name__ == "__main__":
    main()
