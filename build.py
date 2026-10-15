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

FONTS = ("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700"
         "&family=IBM+Plex+Serif:ital,wght@0,400;0,500;0,600;1,400&display=swap")


import hashlib
JS_V = hashlib.md5((Path(__file__).parent / "assets" / "site.js").read_bytes()).hexdigest()[:8]
CSS_V = hashlib.md5((Path(__file__).parent / "assets" / "style.css").read_bytes()).hexdigest()[:8]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


BOOKS_LINK = '<a href="{up}books.html">📖 книги</a>' if (ROOT / "content" / "books.txt").exists() and any(l.strip() and not l.lstrip().startswith("#") for l in (ROOT / "content" / "books.txt").read_text(encoding="utf-8").splitlines()) else ""


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
<meta property="og:url" content="{SITE_URL}/{path}">
<meta property="og:site_name" content="Роман Понуров">
<meta property="og:locale" content="ru_RU">
<meta property="og:image" content="{SITE_URL}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Роман Понуров — менеджер продукта: +103% выручки e-com, 10 млн пользователей MTS ID, 4 продукта с нуля">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE_URL}/assets/og.png">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{up}assets/style.css?v={CSS_V}">
<script>try{{const t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t;}}catch(e){{}}</script>
<script src="{up}assets/site.js?v={JS_V}" defer data-root="{up}"></script>
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="{up}index.html"><img class="avatar avatar-sm" src="{up}assets/avatar-sm.jpg" width="34" height="34" alt="">Роман Понуров</a>
<nav class="nav" aria-label="Разделы">
<details class="menu"><summary>продакт</summary><div class="menu-list"><a href="{up}about.html">👋 обо мне</a><a href="{up}cv.html">📄 резюме</a><a href="{up}cases/index.html">📁 портфолио кейсов</a></div></details>
<a href="{up}projects.html">проекты</a>
<details class="menu"><summary>наука</summary><div class="menu-list"><a href="{up}research.html">🎓 исследования</a><a href="{up}study.html">📚 учёба</a>{BOOKS_LINK.format(up=up)}</div></details>
<a href="{up}agents.html">ИИ-агенты</a>
<a href="{up}blog/index.html">посты</a>
<a href="{up}tags/index.html">теги</a>
</nav>
<span class="tools">
<button type="button" class="icon-btn" id="search-open" aria-label="Поиск по сайту" title="Поиск (/)"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg></button>
<button type="button" class="icon-btn" id="theme-toggle" aria-label="Переключить тёмную тему" title="Тёмная тема"><svg class="i-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg><svg class="i-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></button>
</span>
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
    root = prefix[:-5] if prefix.endswith("blog/") else "../"
    out = []
    for p in posts:
        thumb = f'<img class="feed-thumb" src="{root}{p["cover"]}" alt="" loading="lazy">' if p["cover"] else ""
        rating = f'<span class="feed-rating"><b>{esc(p["rating"])}</b>/10</span>' if p["rating"] else ""
        cat = ('<span class="feed-cat">' + esc(p['tags'][0]) + '</span>') if p['tags'] else ''
        out.append(f"""<li class="feed-item"><a class="feed-link" href="{prefix}{p['slug']}.html">
<span class="feed-meta">{cat}<span>{max(1, round(len(p['body'].split()) / 180))} мин</span><time datetime="{p['date']}">{p['date_h']}</time></span>
<span class="feed-row">{thumb}<span class="feed-body"><span class="feed-title">{esc(p['title'])}</span>
<span class="feed-excerpt">{esc(p['excerpt'])}</span>{rating}</span></span></a></li>""")
    return "\n".join(out)


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
<p class="roles"><a href="cv.html">менеджер продукта</a>, <a href="tags/{tag_slug('преподавание')}.html">начинающий преподаватель</a>, <a href="research.html">исследую ИИ в управлении компанией</a></p>
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
            "stage": meta.get("stage", ""),
            "cover": meta.get("cover", "") if meta.get("cover") and (ROOT / meta["cover"]).exists() else "",
            "rating": meta.get("rating", ""),
            "excerpt": text, "body": body,
        })
    return sorted(posts, key=lambda p: p["date"], reverse=True)


def post_list(posts: list[dict], prefix: str) -> str:
    return "\n".join(
        f"""<li class="post-item"><time datetime="{p['date']}">{p['date_h']}</time>
<div><h3><a href="{prefix}{p['slug']}.html">{esc(p['title'])}</a></h3>
<p>{esc(p['excerpt'])}</p></div></li>"""
        for p in posts)


def book_head(p: dict) -> str:
    if not (p["cover"] or p["rating"]):
        return ""
    img = f'<img class="book-cover" src="../{p["cover"]}" alt="Обложка книги">' if p["cover"] else ""
    rating = f'<p class="feed-rating book-rating"><b>{esc(p["rating"])}</b>/10 — моя оценка</p>' if p["rating"] else ""
    return f'<div class="book-head">{img}{rating}</div>'


def post_thumb(p: dict) -> str:
    if p["cover"]:
        return "../" + p["cover"]
    m = re.search(r'<img src="\.\./([^"]+)"', p["body"])
    return "../" + m.group(1) if m else ""


def short_date(p: dict) -> str:
    y, mo, d = (int(x) for x in p["date"].split("-"))
    return f"{d} {MONTHS_SHORT[mo - 1]} {y} г."


MONTHS_SHORT = ["янв.", "февр.", "мар.", "апр.", "мая", "июн.", "июл.", "авг.", "сент.", "окт.", "нояб.", "дек."]


def post_links(p: dict, posts: list[dict]) -> list[tuple[str, str, str]]:
    """Связи поста: куда он ссылается внутри сайта и какие посты ссылаются на него."""
    out = []
    names = {"agents.html": "ИИ-агенты", "projects.html": "Проекты", "study.html": "Учёба", "research.html": "Исследования",
             "cv.html": "Резюме", "about.html": "Обо мне", "books.html": "Книги", "cases/index.html": "Портфолио кейсов"}
    for text, href in re.findall(r"\[([^\]]+)\]\((\.\./[^)]+|[a-z0-9-]+\.html)\)", p["body"]):
        target = href[3:] if href.startswith("../") else "blog/" + href
        label = names.get(target)
        if target.startswith("blog/"):
            label = next((q["title"] for q in posts if f'blog/{q["slug"]}.html' == target), text)
        elif target.startswith("cases/") and target != "cases/index.html":
            label = case_title(target[6:-5]) if target[6:-5] in [c[0] for c in CASES] else text
        out.append(("→", label or text, "../" + target))
    for q in posts:
        if q is not p and re.search(rf"\({re.escape(p['slug'])}\.html\)|/blog/{re.escape(p['slug'])}\.html|\.\./blog/{re.escape(p['slug'])}\.html", q["body"]):
            out.append(("←", q["title"], f'{q["slug"]}.html'))
    seen, uniq = set(), []
    for d, t, u in out:
        if (d, u) not in seen:
            seen.add((d, u)); uniq.append((d, t, u))
    return uniq


def post_footer(p: dict, posts: list[dict]) -> str:
    others = [q for q in posts if q is not p]
    others.sort(key=lambda q: (-len(set(q["tags"]) & set(p["tags"])), q["date"]), reverse=False)
    others.sort(key=lambda q: (len(set(q["tags"]) & set(p["tags"])), q["date"]), reverse=True)
    cards = []
    for q in others[:4]:
        th = post_thumb(q)
        img = f'<img src="{th}" alt="" loading="lazy">' if th else '<span class="rel-ph" aria-hidden="true"></span>'
        tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in q["tags"][:2])
        cards.append(f"""<a class="rel-card" href="{q['slug']}.html">{img}<span class="rel-body">
<span class="rel-title">{esc(q['title'])}</span>
<span class="rel-meta"><time datetime="{q['date']}">{short_date(q)}</time>{tags}</span></span></a>""")
    links = post_links(p, posts)
    rel = f'<section class="related-posts"><h2>Похожие посты</h2><div class="rel-grid">{"".join(cards)}</div></section>' if cards else ""
    li = "".join(f'<li><span class="dir">{d}</span><a href="{u}">{esc(t)}</a></li>' for d, t, u in links)
    conn = (f'<details class="pill-btn conn"><summary><span class="tri">▸</span> показать связи поста <span class="cnt">{len(links)}</span></summary>'
            f'<ul class="conn-list">{li}</ul><p class="conn-hint">→ куда ссылается пост · ← кто ссылается на него</p></details>') if links else ""
    return f"""{rel}
<div class="post-actions">{conn}<a class="pill-btn" href="https://t.me/astro090"><span aria-hidden="true">✈</span> обсудить в Telegram</a></div>"""


def post_page(p: dict, all_posts: list[dict] | None = None) -> str:
    body_html = markdown.markdown(p["body"], extensions=["tables", "sane_lists"])
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in p["tags"])
    body = f"""
<article class="page"><div class="wrap">
<a class="back" href="index.html">Все посты</a>
<h1>{esc(p['title'])}</h1>
<p class="post-meta"><time datetime="{p['date']}">{p['date_h']}</time>{tags}</p>
{book_head(p)}<div class="prose">
{body_html}
</div>
{post_footer(p, all_posts or [])}
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


CASES_SHOWN = 6
OWN_SLUGS = {"po-sosedstvu", "dobster", "bolz"}  # собственные проекты — на странице «Проекты», не в портфолио


def cases_index_page() -> str:
    cards = []
    work = [c for c in CASES if c[0] not in OWN_SLUGS]
    for i, (slug, company, years, _kind, about, result) in enumerate(work):
        sph, mod, (big, small, color) = TAGS[slug]
        meta = " · ".join([company] + sph + mod)
        hidden = " hidden" if i >= CASES_SHOWN else ""
        cards.append(f"""<li class="card case-card"{hidden}>
<a class="cover" href="{slug}.html" style="background:{color}" aria-hidden="true" tabindex="-1">
<span class="cover-big">{esc(big)}</span><span class="cover-small">{esc(small)}</span></a>
<p class="card-meta">{esc(meta)}</p>
<h2 class="card-title"><a href="{slug}.html">{esc(case_title(slug))}</a></h2>
</li>""")
    more = len(work) - CASES_SHOWN
    more_btn = (f'<button type="button" class="pill-btn more-btn" id="more">смотреть дальше <span class="cnt">{more}</span></button>'
                if more > 0 else "")
    body = f"""
<article class="page"><div class="wrap">
<a class="back" href="../index.html">На главную</a>
<h1>Портфолио кейсов</h1>
<p class="intro">Продукты, которые я запускал и развивал на основной работе: в банке, телекоме, ритейле и госсекторе. Каждый кейс открывается отдельно: контекст, что я сделал и к чему это привело. Собственные продукты — на странице <a href="../projects.html">«Проекты»</a>.</p>
<ul class="cards">
{chr(10).join(cards)}
</ul>
{more_btn}
<div class="xlinks">
<a class="xlink" href="../projects.html"><b>Проекты</b><span>что строил сам и зачем — свои продукты и AI-прототипы</span></a>
<a class="xlink" href="../agents.html"><b>ИИ-агенты</b><span>путь от теории к практике, код и заметки</span></a>
</div>
</div></article>
<script>
(() => {{
  const btn = document.getElementById('more');
  if (btn) btn.addEventListener('click', () => {{
    document.querySelectorAll('.case-card[hidden]').forEach(c => c.hidden = false);
    btn.remove();
  }});
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
<li><span class="when">Сентябрь 2026<br>доклад</span><span class="what"><a href="https://naukaip.ru/wp-content/uploads/2026/09/MK-2774.pdf">Организационная готовность российских компаний к внедрению искусственного интеллекта в систему менеджмента: барьеры и направления развития</a><i>XVI Международная научно-практическая конференция «Развитие современной науки и образования: актуальные вопросы, достижения и инновации», Пенза</i></span></li>
<li><span class="when">2026<br>доклад</span><span class="what"><a href="https://sibac.info/conf/economy/cx/430396">Организационно-управленческие механизмы снижения рисков применения искусственного интеллекта в банковском менеджменте</a><i>CX Международная научно-практическая конференция «Актуальные вопросы экономических наук и современного менеджмента», Новосибирск</i></span></li>
<li><span class="when">Март 2026<br>доклад</span><span class="what"><a href="https://sibac.info/conf/economy/civ/403674">Технологические требования к инфраструктуре компании при внедрении искусственного интеллекта</a><i>CIV Международная научно-практическая конференция «Актуальные вопросы экономических наук и современного менеджмента», Новосибирск</i></span></li>
<li><span class="when">Декабрь 2025<br>ВАК, К2</span><span class="what"><a href="https://s-lib.com/issues/eiu_2025_10_v13_a28/">Риски и ограничения применения искусственного интеллекта в управлении компанией</a><i>Экономика и управление: проблемы, решения</i></span></li>
<li><span class="when">Сентябрь 2025<br>ВАК, К2</span><span class="what"><a href="https://www.finance-man.ru/index.php/journal/article/view/2105">Современные тенденции использования искусственного интеллекта в корпоративном управлении в период цифровой трансформации</a><i>Финансовый менеджмент</i></span></li>
<li><span class="when">Май 2025<br>ВАК, К2</span><span class="what"><a href="https://s-lib.com/issues/eiu_2025_06_v7_a26/">Характерные особенности применения искусственного интеллекта в менеджменте российских компаний</a><i>Экономика и управление: проблемы, решения</i></span></li>
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
    ("Независимая оценка", [
        ("Assessty для МТС · апрель 2022", "Оценка компетенций менеджера продукта",
         "Грейд Middle. Сильнее всего — создание новых продуктов в условиях неопределённости. 17 тем на 8–10 из 10: управление ценностью, бизнес-модель и монетизация, ключевые метрики, гипотезы, UX-тестирование, сроки, риски, груминг.", "ассессмент"),
    ]),
    ("Курсы", [
        ("Pendo.io · 2023", "AI for Product Management", "Как применять ИИ в работе продакт-менеджера и в самих продуктах.", "курс"),
        ("Google · 2023", "Основы интернет-маркетинга", "Каналы привлечения, поисковая и контекстная реклама, веб-аналитика.", "курс"),
        ("GoPractice · 2022", "Симулятор управления продуктом", "Продуктовая аналитика и метрики на сквозном кейсе: от гипотезы до решения по данным.", "курс"),
    ]),
    ("Акселераторы и конкурсы", [
        ("Московский инновационный кластер · июнь–сентябрь 2025", "Акселератор «Академия инноваторов»",
         "Прошёл программу с собственным продуктом bolz — агрегатором шеринг-сервисов: упаковка идеи, проверка гипотез, питч перед экспертами.", "акселератор"),
        ("Москва · июль–август 2025", "Конкурс «Новатор Москвы 2025»",
         "Участвовал с тем же продуктом — bolz.", "конкурс"),
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


def about_page() -> str:
    body = """
<article class="page"><div class="wrap">
<a class="back" href="index.html">На главную</a>
<h1>Обо мне</h1>
<div class="prose about">
<p>Привет 👋 Эта страница — короткая инструкция по работе со мной. Она для коллег, команды и всех, с кем мы начинаем что-то делать вместе: <b>чтобы меньше времени уходило на притирку и больше — на продукт</b>.</p>

<h2>Чем я занимаюсь</h2>
<p>Днём я менеджер продукта, а в аспирантуре РАНХиГС пишу диссертацию на тему <b>«Использование искусственного интеллекта для совершенствования системы управления компанией»</b>. Это одна и та же тема с двух сторон: на работе я строю сервис с ИИ-агентом для кредитного анализа, а в исследовании разбираюсь, как ИИ меняет не отдельные задачи, а само управление — планирование, принятие решений, контроль и коммуникации внутри компании.</p>
<p>Меня интересуют три вопроса:</p>
<ul>
<li>в каких управленческих процессах ИИ действительно даёт эффект, а где это мода;</li>
<li>какие риски и ограничения он приносит — от качества данных до ответственности за решение;</li>
<li>что компании нужно подготовить заранее: данные, инфраструктуру, людей и правила.</li>
</ul>
<p>Об этом мои <a href="research.html">статьи и доклады</a>, а практическую сторону я разбираю в разделе <a href="agents.html">«ИИ-агенты»</a>.</p>

<h2>Во что я верю</h2>
<ul>
<li>Гипотеза → проверка → решение</li>
<li>Одна главная метрика на эксперимент</li>
<li>Бизнес-результат важнее количества фич</li>
<li>ИИ усиливает управление, но не снимает ответственность с человека</li>
<li>Сначала процесс и данные, потом модель</li>
<li>AI — там, где он даёт измеримую ценность, а не ради AI</li>
</ul>

<h2>Как со мной работать</h2>
<p><b>Начинаю с «зачем».</b> Прежде чем обсуждать решение, спрошу, какую проблему пользователя или бизнеса мы решаем и как поймём, что решили. Это не недоверие, а привычка.</p>
<p><b>Люблю цифры и факты.</b> Мнение без данных — нормальная отправная точка, но решение я хочу принимать по результатам кастдева, аналитики или эксперимента.</p>
<p><b>Про ИИ — трезво.</b> Если предлагаете «добавить ИИ», я спрошу, какой процесс он улучшит, как мы измерим эффект и кто отвечает за ошибку модели. Если ответы есть — я первый за.</p>
<p><b>Обратную связь — прямо.</b> Если что-то не так в продукте, процессе или в моей работе, скажите сразу и по делу. Сам даю обратную связь так же: конкретно и с предложением, что поменять.</p>
<p><b>Плохие новости — рано.</b> Сорванный срок, о котором я узнал за неделю, — это план Б. Тот же срок, о котором я узнал в день релиза, — это пожар.</p>
<p><b>Связь.</b> Быстрее всего отвечаю в Telegram. Письма читаю, но не мгновенно. Если срочно — так и напишите.</p>
<p><b>Встречи.</b> У встречи должна быть цель и итог: в конце фиксируем, кто что делает и к какому сроку.</p>
<p class="about-rule">Если сомневаетесь, писать мне или нет, — пишите.</p>
</div>
<p class="related-row">Ещё обо мне: <a href="cv.html">резюме</a> · <a href="cases/index.html">портфолио кейсов</a> · <a href="research.html">исследования</a> · <a href="agents.html">ИИ-агенты</a></p>
</div></article>
"""
    return layout("Обо мне — Роман Понуров", "Как со мной работать: принципы, обратная связь, связь и встречи.", body, "about.html")


def load_books() -> list[dict]:
    """content/books.txt: одна книга на строку — Тема | Название | Автор | Чем полезна | slug поста-рецензии (необязательно)."""
    f = ROOT / "content" / "books.txt"
    books = []
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            parts = [x.strip() for x in line.split("|")] + [""] * 5
            books.append({"topic": parts[0], "title": parts[1], "author": parts[2], "note": parts[3], "post": parts[4]})
    return books


def books_page(books: list[dict], posts: list[dict]) -> str:
    reviews = [p for p in posts if "книги" in p["tags"]]
    blocks = []
    if reviews:
        blocks.append(f'<section class="uni"><div class="uni-head"><h2>Рецензии</h2></div><ul class="feed">{feed(reviews, "blog/")}</ul></section>')
    topics: dict[str, list[dict]] = {}
    for b in books:
        topics.setdefault(b["topic"] or "Разное", []).append(b)
    for topic, items in topics.items():
        lis = "\n".join(
            f'<li><span class="when">{esc(b["author"])}</span><span class="what">'
            + (f'<a href="blog/{b["post"]}.html">{esc(b["title"])}</a>' if b["post"] else esc(b["title"]))
            + (f'<i>{esc(b["note"])}</i>' if b["note"] else "") + "</span></li>"
            for b in items)
        blocks.append(f'<section class="uni"><div class="uni-head"><h2>{esc(topic)}</h2></div><ul class="pubs">\n{lis}\n</ul></section>')
    body = f"""
<article class="page"><div class="wrap">
<a class="back" href="index.html">На главную</a>
<h1>Книги</h1>
<p class="intro">Книги, которые повлияли на то, как я делаю продукты и управляю командами. По главным — пишу рецензии с основными тезисами.</p>
{"".join(blocks)}
</div></article>
"""
    return layout("Книги — Роман Понуров", "Книги о продукте, ИИ и менеджменте, которые читает Роман Понуров, и рецензии на них.", body, "books.html")


WP = GITHUB + "/weekend-planner"
AGENT_STAGES = [
    # (номер, название, что это, практика: [(подпись, ссылка)], статус)
    (1, "Как устроены LLM", "Токены, контекст, температура, почему модель «галлюцинирует» и как писать промпты, которые работают стабильно.", [], "теория"),
    (2, "Структурированный ответ и инструменты", "Модель отвечает не текстом, а JSON по схеме и сама решает, какой инструмент вызвать: погоду, афишу, поиск.",
     [("схемы ответов и цикл вызова инструментов в Планировщике", WP + "/tree/main/weekend_agent/agents")], "есть практика"),
    (3, "Агентный цикл", "Агент сам планирует шаги, вызывает инструменты, проверяет результат и решает, что делать дальше. Где нужен агент, а где хватит обычного сценария.",
     [("разведчик, планировщик и критик", WP + "/tree/main/weekend_agent/agents")], "есть практика"),
    (4, "MCP — протокол инструментов", "Стандартный способ подключить к модели внешние инструменты и данные, чтобы не писать интеграцию заново под каждого агента.",
     [("собственный MCP-сервер с четырьмя инструментами", WP + "/blob/main/weekend_agent/mcp_server.py")], "есть практика"),
    (5, "Мультиагентность и A2A", "Несколько агентов с разными ролями договариваются между собой по протоколу Agent-to-Agent.",
     [("агенты Планировщика общаются по A2A", WP + "/tree/main/weekend_agent/a2a")], "есть практика"),
    (6, "Браузерные агенты", "Агент открывает страницы, читает и действует на сайте там, где нет API.",
     [("браузерный инструмент разведчика", WP + "/blob/main/weekend_agent/tools/providers.py")], "есть практика"),
    (7, "Оркестрация и восстановление", "Что делать, когда инструмент упал, модель ответила мусором или зациклилась: повторы, запасные модели, проверки, ограничение шагов.",
     [("повторы и запасные провайдеры", WP + "/blob/main/weekend_agent/resilience.py")], "есть практика"),
    (8, "Эвалы", "Как измерить качество агента: набор кейсов, автоматические проверки, сравнение версий до и после изменений.",
     [("32 эвал-кейса", WP + "/tree/main/evals")], "есть практика"),
    (9, "Продуктовые метрики агента", "Agent-native метрики: доля задач, решённых без человека, стоимость и время ответа, возвраты и оценки пользователей.",
     [("воронка, retention и оценки в боте", WP + "/blob/main/weekend_agent/analytics/metrics.py")], "есть практика"),
    (10, "Память и RAG", "Как агенту помнить пользователя и опираться на свои документы, а не только на знания модели.", [], "впереди"),
    (11, "Наблюдаемость и безопасность", "Трейсы, логи и стоимость каждого шага; защита от prompt injection и опасных действий.", [], "впереди"),
    (12, "Агент в продакшене", "Запуск на реальных пользователях: A/B-тесты, мониторинг качества, экономика агента.", [], "впереди"),
]


def agents_page(posts: list[dict]) -> str:
    ap = [p for p in posts if "ИИ-агенты" in p["tags"]]
    general = [p for p in ap if not p["stage"]]
    stages = []
    for n, name, what, practice, status in AGENT_STAGES:
        sp = [p for p in ap if p["stage"] == str(n)]
        prac = "".join(f'<li>Практика: <a href="{u}">{esc(t)}</a></li>' for t, u in practice)
        notes = "".join(f'<li>Пост: <a href="blog/{p["slug"]}.html">{esc(p["title"])}</a></li>' for p in sp)
        links = f'<ul class="stage-links">{prac}{notes}</ul>' if prac or notes else ""
        cls = {"есть практика": "done", "впереди": "next"}.get(status, "theory")
        stages.append(f"""<li class="stage stage-{cls}"><span class="stage-n">{n:02d}</span><div>
<h3>{esc(name)} <span class="stage-status">{esc(status)}</span></h3>
<p>{esc(what)}</p>{links}</div></li>""")
    body = f"""
<article class="page"><div class="wrap">
<a class="back" href="index.html">На главную</a>
<h1>ИИ-агенты</h1>
<p class="intro">Здесь я рассказываю свой путь в ИИ-агентах: от теории к практике. Каждый этап — что это такое, где я это попробовал руками и что понял. Главный полигон — <a href="projects.html">Планировщик выходных</a>, агентный Telegram-бот с открытым кодом.</p>

{('<h2>Последние заметки</h2><ul class="feed">' + feed(general + [p for p in ap if p["stage"]], "blog/") + '</ul>') if ap else ''}

<h2 class="stages-head">Карта пути</h2>
<ol class="stages">
{"".join(stages)}
</ol>
</div></article>
"""
    return layout("ИИ-агенты — Роман Понуров", "Путь изучения ИИ-агентов от теории к практике: LLM, инструменты, MCP, A2A, эвалы, метрики.", body, "agents.html")


def build_search_index() -> None:
    """search.json: заголовок, адрес, раздел и текст каждой страницы — для поиска в браузере."""
    import json
    kinds = {"blog": "пост", "cases": "кейс"}
    items = []
    for f in sorted(ROOT.rglob("*.html")):
        rel = f.relative_to(ROOT).as_posix()
        if rel.startswith(("tags/", "content/", "tools/")) or re.match(r"page\d+\.html$", rel) or rel in ("blog/index.html", "index.html"):
            continue
        html_ = f.read_text(encoding="utf-8")
        title = html.unescape(re.search(r"<title>(.*?)</title>", html_).group(1)).replace(" — Роман Понуров", "").replace(" — кейс Романа Понурова", "")
        main_ = re.search(r"<main>(.*)</main>", html_, re.S).group(1)
        main_ = re.sub(r"<(script|style|nav)\b.*?</\1>", " ", main_, flags=re.S)
        main_ = re.sub(r'<section class="related-posts">.*?</section>|<div class="post-actions">.*?</div>|<a class="back"[^>]*>.*?</a>|<p class="post-meta">.*?</p>', " ", main_, flags=re.S)
        text = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", main_))).strip()
        kind = kinds.get(rel.split("/")[0], "страница") if "/" in rel else "страница"
        items.append({"t": title, "u": rel, "k": kind, "x": text[:6000]})
    (ROOT / "search.json").write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    posts = load_posts()
    pages = max(1, -(-len(posts) // PER_PAGE))
    for n in range(1, pages + 1):
        (ROOT / ("index.html" if n == 1 else f"page{n}.html")).write_text(index_page(posts, n), encoding="utf-8")
    (ROOT / "cv.html").write_text(cv_page(), encoding="utf-8")
    (ROOT / "projects.html").write_text(projects_page(), encoding="utf-8")
    (ROOT / "research.html").write_text(research_page(), encoding="utf-8")
    (ROOT / "study.html").write_text(study_page(), encoding="utf-8")
    (ROOT / "about.html").write_text(about_page(), encoding="utf-8")
    (ROOT / "agents.html").write_text(agents_page(posts), encoding="utf-8")
    books = load_books()
    if books:
        (ROOT / "books.html").write_text(books_page(books, posts), encoding="utf-8")
    for d in ("blog", "cases", "tags"):
        (ROOT / d).mkdir(exist_ok=True)
    for f in (ROOT / "tags").glob("*.html"):
        f.unlink()
    for name, html_ in tags_pages(posts).items():
        (ROOT / "tags" / name).write_text(html_, encoding="utf-8")
    (ROOT / "blog" / "index.html").write_text(blog_index_page(posts), encoding="utf-8")
    for p in posts:
        (ROOT / "blog" / f"{p['slug']}.html").write_text(post_page(p, posts), encoding="utf-8")
    (ROOT / "cases" / "index.html").write_text(cases_index_page(), encoding="utf-8")
    for i, case in enumerate(CASES):
        (ROOT / "cases" / f"{case[0]}.html").write_text(case_page(i), encoding="utf-8")
    build_search_index()
    print(f"Готово: главная, {len(posts)} пост(ов), {len(CASES)} кейсов, резюме, проекты, исследования, теги")


if __name__ == "__main__":
    main()
