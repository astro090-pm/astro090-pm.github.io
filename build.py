"""Сборка сайта-портфолио: python build.py  →  index.html и cases/*.html.

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
     "Внутренний сервис кредитного анализа компаний: от концепции и защиты бюджета до запуска.",
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

FONTS = ("https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600"
         "&family=Unbounded:wght@600;700&display=swap")


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
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="{up}index.html">Роман Понуров</a>
<nav class="nav" aria-label="Разделы">
<a href="{up}index.html#cases">Кейсы</a>
<a href="{up}index.html#ai">AI-проекты</a>
<a href="{up}index.html#research">Исследования</a>
<a href="{up}index.html#contacts">Контакты</a>
</nav>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">Роман Понуров, менеджер продукта. Исходники сайта — <a href="{GITHUB}/astro090-pm.github.io">на GitHub</a>.</div></footer>
</body>
</html>
"""


def index_page() -> str:
    cases_html = "\n".join(
        f"""<li class="case">
<div class="case-when"><b>{esc(company)}</b>{esc(years)}<br>{esc(kind)}</div>
<div><h3><a href="cases/{slug}.html">{esc(case_title(slug))}</a></h3>
<p>{esc(about)}</p>
<p class="result">{esc(result)}</p></div>
</li>"""
        for slug, company, years, kind, about, result in CASES
    )
    body = f"""
<section class="hero"><div class="wrap">
<h1>Роман Понуров</h1>
<p class="lead">Менеджер продукта. Шесть лет запускаю продукты с нуля и вывожу бизнес из офлайна в онлайн.</p>
<p class="lead">Работал в фудтехе, телекоме, финтехе и благотворительности — в B2C, B2B, B2E и B2G. Сейчас строю AI-продукты на агентах и исследую ИИ в управлении компанией.</p>

<div class="ledger" aria-label="Результаты">
<div class="ledger-row"><span class="num">+103%</span><span class="ledger-what">выручки после перезапуска онлайн-доставки продуктов</span><span class="ledger-where"><a href="cases/asia-online.html">Азия Онлайн, 2023–2024</a></span></div>
<div class="ledger-row"><span class="num">10 млн</span><span class="ledger-what">пользователей входят в 9 продуктов МТС через одну авторизацию</span><span class="ledger-where"><a href="cases/mts-id.html">MTS ID, 2021–2023</a></span></div>
<div class="ledger-row"><span class="num">+89%</span><span class="ledger-what">заказов от бизнес-клиентов после выхода магазина в онлайн</span><span class="ledger-where"><a href="cases/po-sosedstvu.html">По соседству, 2022–2024</a></span></div>
<div class="ledger-row"><span class="num">4</span><span class="ledger-what">продукта запущены с нуля, два из них — как сооснователь</span><span class="ledger-where"><a href="#cases">все кейсы</a></span></div>
</div>
</div></section>

<section class="block" id="cases"><div class="wrap">
<h2>Продуктовые кейсы</h2>
<p class="intro">Код рабочих проектов принадлежит компаниям, поэтому здесь описания: контекст, что я сделал и к чему это привело.</p>
<ul class="cases">
{cases_html}
</ul>
</div></section>

<section class="block" id="ai"><div class="wrap">
<h2>AI-проекты</h2>
<p class="intro">Прототипы, на которых я проверяю гипотезы про AI-продукты. Код открыт.</p>
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
</div></section>

<section class="block" id="research"><div class="wrap">
<h2>Исследования</h2>
<p class="intro">Аспирантура РАНХиГС, менеджмент, 2024–2027. Тема диссертации — использование искусственного интеллекта для совершенствования системы управления компанией.</p>
<ul class="pubs">
<li><span class="when">Март 2026<br>доклад</span><span class="what">Технологические требования к инфраструктуре компании при внедрении искусственного интеллекта<i>CIV Международная научно-практическая конференция «Актуальные вопросы экономических наук и современного менеджмента»</i></span></li>
<li><span class="when">Декабрь 2025<br>ВАК, К2</span><span class="what">Риски и ограничения применения искусственного интеллекта в управлении компанией<i>Экономика и управление: проблемы, решения</i></span></li>
<li><span class="when">Сентябрь 2025<br>ВАК, К2</span><span class="what">Современные тенденции использования искусственного интеллекта в корпоративном управлении в период цифровой трансформации<i>Финансовый менеджмент</i></span></li>
<li><span class="when">Май 2025<br>ВАК, К2</span><span class="what">Характерные особенности применения искусственного интеллекта в менеджменте российских компаний<i>Экономика и управление: проблемы, решения</i></span></li>
</ul>
</div></section>

<section class="block" id="path"><div class="wrap">
<h2>Путь</h2>
<p class="intro">Из инженерии — в системный анализ, оттуда — в продакт-менеджмент.</p>
<ol class="path">
<li><span class="yrs">2014–2019</span>Инженер, затем менеджер по развитию бизнеса</li>
<li><span class="yrs">2019–2021</span>Системный аналитик, затем менеджер продукта — Концерн ГРАНИТ</li>
<li><span class="yrs">2021–2023</span>Менеджер продукта MTS ID — МТС</li>
<li><span class="yrs">2023–2024</span>Руководитель электронной коммерции — Азия Ритейл</li>
<li class="now"><span class="yrs">с 2024</span>Менеджер продукта — Газпромбанк</li>
</ol>
<p class="intro" style="margin-top:24px">Образование: НИУ МЭИ, электротехника (2015) · НИУ ВШЭ, корпоративные финансы (2021) · РАНХиГС, аспирантура по менеджменту (2027).</p>
</div></section>

<section class="block" id="contacts"><div class="wrap">
<h2>Контакты</h2>
<p class="intro">Открыт к разговору о продуктовых и AI-ролях.</p>
<div class="contacts">
<a href="https://t.me/astro090">Telegram: @astro090</a>
<a href="mailto:ponurov.roman@yandex.ru">ponurov.roman@yandex.ru</a>
<a href="{GITHUB}">GitHub</a>
</div>
</div></section>
"""
    return layout("Роман Понуров — менеджер продукта",
                  "Менеджер продукта: 6 лет запусков в B2C, B2B, B2E и B2G, кейсы с результатами и AI-проекты.",
                  body, "")


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
<a class="back" href="../index.html#cases">Все кейсы</a>
<h1>{esc(case_title(slug))}</h1>
<div class="prose">
{body_html}
<p class="next-case">Следующий кейс: <a href="{nxt[0]}.html">{esc(case_title(nxt[0]))}</a></p>
</div>
</div></article>
"""
    return layout(f"{case_title(slug)} — кейс Романа Понурова", about, body, f"cases/{slug}.html", depth=1)


def main() -> None:
    (ROOT / "index.html").write_text(index_page(), encoding="utf-8")
    (ROOT / "cases").mkdir(exist_ok=True)
    for i, case in enumerate(CASES):
        (ROOT / "cases" / f"{case[0]}.html").write_text(case_page(i), encoding="utf-8")
    print(f"Готово: index.html и {len(CASES)} страниц кейсов")


if __name__ == "__main__":
    main()
